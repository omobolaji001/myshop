from decimal import Decimal
from rest_framework import serializers
from cart.cart import Cart
from shop.models import Product
from coupons.models import Coupon
from shop.api.serializers import ProductSerializer


class CartItemSerializer(serializers.Serializer):
    """ Cart item serializer """
    product_id = serializers.IntegerField()
    product = ProductSerializer(read_only=True)
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )


class CartSerializer(serializers.Serializer):
    """ Cart serializer """
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    coupon_id = serializers.IntegerField(read_only=True, allow_null=True)
    discount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    total_price_after_discount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    def to_representation(self, cart):
        """ Returns the cart details """
        items = []

        for item in cart:
            items.append({
                'product_id': str(item['product'].id),
                'product': ProductSerializer(item['product']).data,
                'quantity': item['quantity'],
                'price': item['price'],
                'total_price': item['total_price']
            })

        return {
            'items': items,
            'total_price': cart.get_total_price(),
            'coupon_id': cart.coupon_id,
            'discount': cart.get_discount(),
            'total_price_after_discount': cart.get_total_price_after_discount()
        }
