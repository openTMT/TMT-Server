from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from tmtapp.zentao import Zentao


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
            request.session['user'] = user_info
            request.session['zid'] = zid
            return Response({"status": True, "message": "成功", "data": user_info})
        else:
            return Response({"status": False, "message": "失败", "data": {}})

    def delete(self, request):
        """
        用户退出登录
        """
        del request.session['user']
        return Response({"status": True, "message": "成功", "data": {}})
