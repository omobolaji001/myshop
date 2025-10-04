from rest_framework import serializers
from orders.models import Order, OrderItem
from shop.models import Product
from shop.api.serializers import ProductSerializer
from coupons.models import Coupon
from decimal import Decimal


class OrderItemSerializer(serializers.ModelSerializer):
    """ Serializes the order item """
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        """ Metadata """
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    """ Serializes the order """
    items = OrderItemSerializer(many=True, read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    address = serializers.CharField(required=True)
    postal_code = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    total = serializers.SerializerMethodField()

    class Meta:
        """ Metadata """
        model = Order
        fields = [
            'id', 'first_name', 'last_name', 'email',
            'address', 'postal_code', 'city', 'items',
            'total', 'total', 'coupon', 'discount',
            'created', 'updated', 'paid', 'stripe_id'
        ]

    def get_total(self, obj):
        """ Return total cost """
        return obj.get_total_cost()

    def validate(self, data):
        """ Ensure discount and coupon consistency """
        if data.get('discount') and not data.get('coupon'):
            raise serializers.ValidationError(
                'Discount cannot be applied without a coupon'
            )
        if data.get('coupon') and not data.get('discount'):
            raise serializers.ValidationError(
                'Coupon requires a discount value'
            )

        return data
