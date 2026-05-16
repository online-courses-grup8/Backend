from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = "limit"
    max_page_size = 20

    def get_paginated_response(self, data):
        # projenin {status, payload, errorMessage} formatında döner
        return Response({
            "status": 200,
            "payload": {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            },
            "errorMessage": None
        })