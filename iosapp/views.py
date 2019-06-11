from django.http import Http404
from rest_framework import generics, mixins, views
from rest_framework.response import Response
from .models import *
from django.conf import settings
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import *
from .libimobiledevice import Libimobiledevice
import threading, time

lib_mobile = None


def keep_connect_mac():
    global lib_mobile
    if lib_mobile:
        return lib_mobile
    try:
        lib_mobile = Libimobiledevice()
        return lib_mobile
    except Exception as e:
        lib_mobile = None
        return False


keep_connect_mac()


class DeviceObject(views.APIView):
    """
    设备列表
    """

    def get(self, request):
        """
        设备列表
        """
        devices = iOSDevice.objects.filter(owner__in=('public', request.session['user'].get('username')))
        serializer = iOSDeviceSerializer(devices, many=True)
        return Response({"status": True, "message": "成功", "data": serializer.data})


class DeviceScreenShotObject(views.APIView):
    """
    截屏操作
    """

    def post(self, request, uuid):
        """
        截屏操作
        """
        to = request.session['user'].get('username')

        if not keep_connect_mac():
            return Response({"status": False, "message": "MAC服务器不在线", "data": ""})

        # 执行截图 与 设备信息 操作，并上传
        response = lib_mobile.screenshot_device_info_then_upload(uuid, to)

        if not response.get('file_info'):
            return Response({"status": False, "message": "失败，请检查设备是否在线", "data": ""})

        # 发送消息给人
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(to, {
            "device_info": deal_with_device_info(response.get('device_info')),
            "message": response.get('file_info'),
            "room": f"{to}_ios",
            "to": to,
            "type": "message"
        })

        return Response({"status": True, "message": "成功", "data": ""})


class DeviceLogCatObject(views.APIView):
    """
    抓日志操作
    """

    def post(self, request, uuid):
        """
        抓日志操作
        """
        to = request.session['user'].get('username')
        action = request.data.get('action')

        if not keep_connect_mac():
            return Response({"status": False, "message": "MAC服务器不在线", "data": ""})

        if action == 'start':
            try:
                if lib_mobile.syslog_start(uuid):
                    threading.Thread(target=self.delay_stop, args=(request, uuid,)).start()
                    return Response({"status": True, "message": "成功", "data": ""})
                else:
                    return Response({"status": False, "message": "失败，请检查设备是否在线", "data": ""})
            except Exception as e:
                return Response({"status": False, "message": str(e), "data": ""})

        elif action == 'stop':

            # 执行结束抓日志 与 设备信息 操作，并上传
            response = lib_mobile.syslog_device_info_then_upload(uuid, to)

            if not response.get('file_info'):
                return Response({"status": False, "message": "失败，请检查设备是否在线", "data": ""})

            # 发送消息给人
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(to, {
                "device_info": deal_with_device_info(response.get('device_info')),
                "message": response.get('file_info'),
                "room": f"{to}_ios",
                "to": to,
                "type": "message"
            })
            return Response({"status": True, "message": "成功", "data": ""})
        elif action == 'delay_stop':
            lib_mobile.syslog_stop(uuid)
        else:
            return Response({"status": False, "message": "action指令不正确", "data": ""})

    def delay_stop(self, request, uuid):
        time.sleep(125)
        request.data['action'] = 'delay_stop'
        self.post(request, uuid)


def deal_with_device_info(device_info):
    baseinfo = BaseDeviceInfo.objects.all()
    base_device_info = {}
    for info in baseinfo:
        base_device_info[info.model_id] = info
    return {
        "device_name": base_device_info.get(device_info.get('ProductType')).name,
        "system": f"iOS {device_info.get('ProductVersion')}",
        "screen": base_device_info.get(device_info.get('ProductType')).screen,
        "memory": f"总容量:{round(int(base_device_info.get(device_info.get('ProductType')).ram)/1024.0,2)}GB",
        "storage": f"总容量{round(int(device_info.get('TotalDataCapacity'))/1024.0/1024.0/1024.0,2)}GB,可使用{round(int(device_info.get('TotalDataAvailable'))/1024.0/1024.0/1024.0,2)}GB",
        "charge": f"{device_info.get('BatteryCurrentCapacity')}%",
    }
