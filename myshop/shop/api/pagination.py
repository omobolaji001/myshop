from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """ Sets standard pagination for the shop """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
