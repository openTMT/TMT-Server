from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)  # 获取本来应该返回的exception的response
    if response is not None:
        response.data['status'] = False
        response.data['message'] = response.data['detail']
        response.data['data'] = response.data['detail']
        del response.data['detail']  # 删掉原来的detail
        response.status_code = 200
    return response
