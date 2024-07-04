from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination


class WatchListPagination(PageNumberPagination):
    page_size=10
    page_query_params = 'p'
    page_size_query_param='size'
    max_page_size=10
    last_page_strings='end'    
    

class WatchListLOPagination(LimitOffsetPagination):
    default_limit=5
    
    
class WatchListCursorPagination(CursorPagination):
    page_size=5
    
    