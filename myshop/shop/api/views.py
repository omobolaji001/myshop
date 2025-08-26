from rest_framework import viewsets
from shop.models import Category
from shop.api.serializers import CategorySerializer
from shop.api.pagination import StandardPagination


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ Provides read-only action to list Category objects
    or retrieve a Category object.
    """
    queryset = Category.objects.prefetch_related('products')
    serializer_class = CategorySerializer
    pagination_class = StandardPagination
