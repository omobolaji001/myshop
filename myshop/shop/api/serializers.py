from rest_framework import serializers
from shop.models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    """ Serializer class for the products """

    class Meta:
        """ Metadata """
        model = Product
        fields = [
            'id', 'name', 'slug', 'description',
            'price', 'available', 'created', 'updated'
        ]


class CategorySerializer(serializers.ModelSerializer):
    """ Serializer class for the product category """
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        """ Metadata """
        model = Category
        fields = ['id', 'name', 'slug', 'products']

