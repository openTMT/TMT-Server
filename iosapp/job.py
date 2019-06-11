from .libimobiledevice import Libimobiledevice
import time
from .models import *
from .views import *


def update_iOS_device_status():
    # todo
    # baseinfo = BaseDeviceInfo.objects.all()
    # base_device_info = {}
    # for info in baseinfo:
    #     base_device_info[info.model_id] = info

    libimob = keep_connect_mac()
    if not libimob:
        return
    device_list = libimob.device_list()
    iOS_device_list = iOSDevice.objects.all()
    for ios in iOS_device_list:
        if ios.uuid in device_list:
            if ios.status == '在线':
                continue
            try:
                info = libimob.device_info(ios.uuid)
                ios.model_id = info.get('ProductType')
                ios.personal_name = info.get('DeviceName')
                ios.version = info.get('ProductVersion')
                ios.device_name = base_device_info[info.get('ProductType')].name
            except:
                pass
            ios.status = '在线'
            ios.save()
        else:
            ios.status = '离线'
            ios.save()
    print(device_list)
