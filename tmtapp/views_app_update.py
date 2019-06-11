from rest_framework import generics, views, mixins

from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FileUploadParser
from .serializers import *
from django.conf import settings
import os, time
from .models import *


class AppUploadObject(views.APIView):
    """
    app更新包上传
    """
    serializer_class = AppFileSerializer

    def compare_version(self, a, b):
        """比较两个版本的大小，需要按.分割后比较各个部分的大小"""
        lena = len(a.split('.'))  # 获取版本字符串的组成部分
        lenb = len(b.split('.'))
        a2 = a + '.0' * (lenb - lena)  # b比a长的时候补全a
        b2 = b + '.0' * (lena - lenb)
        print(a2, b2)
        for i in range(max(lena, lenb)):  # 对每个部分进行比较，需要转化为整数进行比较
            if int(a2.split('.')[i]) > int(b2.split('.')[i]):
                return a
            elif int(a2.split('.')[i]) < int(b2.split('.')[i]):
                return b
            else:  # 比较到最后都相等，则返回第一个版本
                if i == max(lena, lenb) - 1:
                    return a

    def get(self, request):
        app_count = AppUpdate.objects.filter(status=1).count()
        if app_count <= 0:
            return Response({"update": 'No', "new_version": "", "apk_file_url": "", "update_log": "", "target_size": "",
                             "new_md5": "", "constraint": False})

        app_info = AppUpdate.objects.filter(status=1).order_by('-id')[0]
        try:
            last_version = self.compare_version(request.query_params.get('version'), app_info.version)
            update = 'NO' if request.query_params.get('version') == last_version else 'Yes'
        except:
            update = 'NO'
        return Response({
            "update": update,
            "new_version": app_info.version,
            "apk_file_url": app_info.file_url,
            "update_log": app_info.update_log,
            "target_size": str(round(int(app_info.file_size) / 1024 / 1024, 2)) + 'MB',
            "new_md5": app_info.md5,
            "constraint": bool(app_info.constraint)
        })

    def post(self, request):
        files = request.FILES.getlist('file', None)
        file_object = files[0]
        file_name_prefix = '.'.join(file_object.name.split('.')[:-1])
        file_name_suffix = file_object.name.split('.')[-1] if '.' in file_object.name else ''
        file_name = f'{str(int((time.time()*1000)))}_{file_name_prefix}.{file_name_suffix}'
        file_dir = os.path.join(settings.BASE_DIR, 'files', 'app')
        if not os.path.exists(file_dir): os.makedirs(file_dir)
        file_path = os.path.join(file_dir, file_name)
        destination = open(file_path, 'wb+')
        for chunk in file_object.chunks():
            destination.write(chunk)
        destination.close()
        file_url = f'{settings.DOMAIN}/files/app/{file_name}'

        AppUpdate.objects.create(
            file_size=file_object.size,
            file_path=file_path,
            file_url=file_url,
            version=request.data.get('version'),
            update_log=request.data.get('update_log'),
            md5="",
            constraint=request.data.get('constraint'),
        )
        return Response({"status": True, "message": "成功", "data": {}})


class AppHistoryObject(generics.GenericAPIView, mixins.ListModelMixin):
    """
    app更新记录
    """
    serializer_class = AppHistorySerializer
    queryset = AppUpdate.objects.filter(status=1).order_by('-id')

    def get(self, request):
        return self.list(request)
