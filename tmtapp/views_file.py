from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FileUploadParser
from .serializers import *
from django.conf import settings
import os, time
from .models import *
from django.http import FileResponse
from django.http import Http404
from django.utils.http import urlquote
import chardet
from .zentao import Zentao


class FileUploadObject(views.APIView):
    """
    上传文件接口(只支持单文件上传)
    """
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request):
        files = request.FILES.getlist('file', None)
        file_object = files[0]
        file_name_prefix = '.'.join(file_object.name.split('.')[:-1])
        file_name_suffix = file_object.name.split('.')[-1] if '.' in file_object.name else ''
        file_name = f'{str(int((time.time()*1000)))}_{file_name_prefix}.{file_name_suffix}'
        file_dir = os.path.join(settings.BASE_DIR, 'files', time.strftime("%Y-%m"))
        if not os.path.exists(file_dir): os.makedirs(file_dir)
        file_path = os.path.join(file_dir, file_name)
        destination = open(file_path, 'wb+')
        for chunk in file_object.chunks():
            destination.write(chunk)
        destination.close()
        file_url = f'{settings.DOMAIN}/files/{time.strftime("%Y-%m")}/{file_name}'

        Files.objects.create(
            username=request.session['user'].get('username') if request.session.get('user') else request.data.get(
                'username'),
            file_name=file_name,
            file_size=file_object.size,
            file_type=file_name_suffix,
            file_path=file_path,
            file_url=file_url,
            device_info=request.data.get('device_info'),
        )
        return Response(
            {"status": True, "message": "成功",
             "data": {"url": file_url, "type": file_name_suffix, "path": file_path, "name": file_name}})


class FileUploadBugObject(views.APIView):
    """
    上传文件接口，为缺陷中的图片
    """
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request):

        files = request.FILES.getlist('file', None)
        file_object = files[0]
        file_name_prefix = '.'.join(file_object.name.split('.')[:-1])
        file_name_suffix = file_object.name.split('.')[-1] if '.' in file_object.name else ''
        file_name = f'{str(int((time.time()*1000)))}_{file_name_prefix}.{file_name_suffix}'
        file_dir = os.path.join(settings.BASE_DIR, 'files', time.strftime("%Y-%m"))
        if not os.path.exists(file_dir): os.makedirs(file_dir)
        file_path = os.path.join(file_dir, file_name)
        destination = open(file_path, 'wb+')
        for chunk in file_object.chunks():
            destination.write(chunk)
        destination.close()
        file_url = f'{settings.DOMAIN}/files/{time.strftime("%Y-%m")}/{file_name}'

        Files.objects.create(
            username=request.session['user'].get('username') if request.session.get('user') else request.data.get(
                'username'),
            file_name=file_name,
            file_size=file_object.size,
            file_type=file_name_suffix,
            file_path=file_path,
            file_url=file_url,
            device_info='{}',
        )

        zid = request.session.get('zid')
        files = {
            'imgFile': (file_name, open(file_path, "rb")),
        }
        issue_file_url = Zentao.upload_file(zid, files)
        issue_file_url = f'{settings.ZENTAO_HOST}{issue_file_url}'
        return Response(
            {"status": True, "message": "成功",
             "data": {"issue_file_url": issue_file_url, "url": file_url, "type": file_name_suffix, "path": file_path,
                      "name": file_name}})
