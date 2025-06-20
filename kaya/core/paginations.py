from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "size"  # items per page
    max_page_size = 100


# def get_paginated_response(queryset, request, serializer_class, context={}):
#     pagination_class = CustomPageNumberPagination
#     paginator = pagination_class()

#     page = paginator.paginate_queryset(queryset, request)
#     serializer = serializer_class(page, context=context, many=True)
#     return paginator.get_paginated_response(serializer.data)