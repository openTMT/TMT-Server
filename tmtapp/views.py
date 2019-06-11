from django.http import Http404
from rest_framework import generics, mixins, views
from rest_framework.response import Response
from .zentao import Zentao
from .bug_template import *
from .serializers import *
from .models import *
from django.conf import settings
import json


class ProductObject(views.APIView):
    """
    产品操作
    """

    def get(self, request):
        """
        获取产品列表
        """
        zid = request.session.get('zid')
        product_list = Zentao.get_product_list(zid)
        return Response({"status": True, "message": "成功", "data": product_list})


class ProjectObject(views.APIView):
    """
    项目操作
    """

    def get(self, request, product_id):
        """
        获取某个产品下的项目列表
        """
        zid = request.session.get('zid')
        project_list = Zentao.get_project_list(zid, product_id)
        return Response({"status": True, "message": "成功", "data": project_list})


class UserObject(views.APIView):
    """
    用户操作
    """

    def get(self, request):
        """
        获取所有用户列表
        """
        zid = request.session.get('zid')
        user_list = Zentao.get_all_users(zid)
        return Response({"status": True, "message": "成功", "data": user_list})


class BugObject(views.APIView):
    """
    bug操作
    """

    def handle_data(self, data):
        # data = {
        #     'product': 27,
        #     'module': 0,
        #     'project': 391,
        #     'openedBuild[]': 'trunk',
        #     'assignedTo': 'chengm',
        #     'type': 'codeerror',
        #     'title': 'bug标题223',
        #     'severity': '3',
        #     'pri': '3',
        #     'steps': '<p>[步骤]</p>1111<br /><p>	[结果]</p>2222<br /><p>	[期望]</p>33333',
        #     'mailto[1]': 'chengm',
        #     'mailto[2]': 'chengm',
        #
        # }
        files = {}
        data['openedBuild[]'] = 'trunk'
        if data.get("title_pre"):
            data['title'] = f"【{data['title_pre']}】{data['title']}"
            del data['title_pre']
        if data.get("title_pre") != None:
            del data['title_pre']
        if data.get("mailto"):
            for i, mailto in enumerate(data.get("mailto")):
                data[f'mailto[{i}]'] = mailto
            del data['mailto']
        if data.get("files"):
            for i, file_info in enumerate(data.get("files")):
                files[f'files[{i}]'] = (file_info['name'], open(file_info['path'], "rb"))
            del data['files']

        if data.get("device_info"):
            data['steps'] += zentao_bug_template.format(data['device_info'].get('device_name'),
                                                        data['device_info'].get('system'),
                                                        data['device_info'].get('charge'),
                                                        data['device_info'].get('screen'),
                                                        data['device_info'].get('memory'),
                                                        data['device_info'].get('storage'),
                                                        )
            del data['device_info']
        return data, files

    def get(self, request):
        """
        获取自己提交的bug
        """
        my_bugs = Bugs.objects.filter(username=request.session['user'].get('username'), status=1).order_by('-id')
        serializer = BugSerializer(my_bugs, many=True)
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def post(self, request):
        """
        提交一个bug
        """
        zid = request.session.get('zid')
        souce_data = request.data.copy()

        image_data = ''
        if souce_data.get("files"):
            for i, file_info in enumerate(souce_data.get("files")):
                if file_info['type'] != 'png': continue
                files = {}
                files['imgFile'] = (file_info['name'], open(file_info['path'], "rb"))
                tmp_url = '/zentao' + Zentao.upload_file(zid, files)
                image_data += f'<br><br><p><img width="400" src="{tmp_url}" alt="image.png" /></p>'
        if image_data != '':
            request.data['steps'] = request.data['steps'] + '<p>[附件]</p>' + image_data

        data, files = self.handle_data(request.data)
        flag, bug_id = Zentao.create_bug(zid, data, files)
        if flag:
            link = f'{settings.ZENTAO_HOST}/bug-view-{bug_id}.html'
            Bugs.objects.create(
                user_id=request.session['user'].get('id'),
                username=request.session['user'].get('username'),
                realname=request.session['user'].get('realname'),
                title=data.get('title'),
                link=link,
                product=data.get('product'),
                project=data.get('project'),
                assignedTo=data.get('assignedTo'),
                type=data.get('type'),
                severity=data.get('severity'),
                pri=data.get('pri'),
                file_count=len(souce_data.get('files')),
                device_info=json.dumps(souce_data.get('device_info'), ensure_ascii=False),
                bug_info=json.dumps(data, ensure_ascii=False),
            )
            return Response({"status": True, "message": "成功", "data": link})
        else:
            return Response({"status": False, "message": "失败", "data": bug_id})
