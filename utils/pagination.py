from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = "limit"
    max_page_size = 20