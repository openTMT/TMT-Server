from rest_framework.pagination import LimitOffsetPagination
from collections import OrderedDict
from rest_framework.response import Response


class LimitOffsetPaginationCustomer(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response({"status": True, "message": "成功",
                         'count': self.count,
                         'next': self.get_next_link(),
                         'previous': self.get_previous_link(),
                         "data": data})
