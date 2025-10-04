from rest_framework import viewsets
from shop.models import Category, Product
from shop.api.serializers import CategorySerializer, ProductSerializer
from shop.api.pagination import StandardPagination


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ Provides read-only action to list Category objects
    or retrieve a Category object.
    """
    queryset = Category.objects.prefetch_related('products')
    serializer_class = CategorySerializer
    pagination_class = StandardPagination


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """ Provides read-only action to list Product objects
    or retrieve a Product object.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardPagination
