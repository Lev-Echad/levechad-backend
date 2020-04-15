from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'pageSize'
    max_page_size = 100
