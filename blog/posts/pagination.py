# posts/pagination.py
from rest_framework.pagination import PageNumberPagination

class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"   # allow ?page_size=20
    max_page_size = 50
    