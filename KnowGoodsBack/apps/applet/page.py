from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response
from collections import OrderedDict
class productgoodsPageNumber(PageNumberPagination):
    page_size = 6
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 10

    # 重写get_paginated_response方法
    def get_paginated_response(self,data):
        return Response(OrderedDict([
            ('code', 200),  # 修改1
            ('msg', '查询成功'),  # 修改2
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

from rest_framework.mixins import ListModelMixin
class CustomListModelMixin(ListModelMixin):
    """
    继承ListModelMixin重写list方法
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = {"code": 200, "msg": '成功', "result": serializer.data}  # 修改一
        return Response(data)  # 修改二
