from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from tmtapp.zentao import Zentao
from .models import Users
from .serializers import UsersSerializer


class UserAuth(APIView):
    """
    登录鉴权
    """

    def get(self, request):
        if request.session.get('user'):
            return Response({"status": True, "message": "成功", "data": request.session.get('user')})
        else:
            return Response({"status": False, "message": "失败", "data": {}})

    def post(self, request):
        """
        用户登录鉴权，通过zentao
        """
        username = request.data.get('username')
        password = request.data.get('password')

        zid, user_info = Zentao.login(username, password)
        if user_info:
            info, created = Users.objects.get_or_create(username=username)
            info.realname = user_info.get('realname')
            info.email = user_info.get('email')
            info.save()
            serializer = UsersSerializer(info)
            request.session['user'] = serializer.data
            request.session['zid'] = zid
            return Response({"status": True, "message": "成功", "data": serializer.data})
        else:
            return Response({"status": False, "message": "失败", "data": {}})

    def delete(self, request):
        """
        用户退出登录
        """
        del request.session['user']
        return Response({"status": True, "message": "成功", "data": {}})
