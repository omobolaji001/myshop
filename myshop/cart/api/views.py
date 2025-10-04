from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from cart.cart import Cart
from cart.api.serializers import CartSerializer
from shop.models import Product
from coupons.models import Coupon
from django.utils import timezone


class CartViewSet(viewsets.ViewSet):
    """ Cart viewset """
    permission_classes = [AllowAny]


    @action(detail=False, methods=['get'])
    def cart_detail(self, request):
        """ Get current cart """
        cart = Cart(request)
        serializer = CartSerializer(cart)

        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add(self, request):
        """ Add or update an item to the cart """
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        override_quantity = request.data.get('override_quantity', False)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        cart = Cart(request)
        cart.add(
            product=product,
            quantity=quantity,
            override_quantity=override_quantity
        )
        serializer = CartSerializer(cart)

        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def remove(self, request):
        """ Remove an item from the cart """
        product_id = request.data.get('product_id')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        cart = Cart(request)
        cart.remove(product)
        serializer = CartSerializer(cart)

        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def apply_coupon(self, request):
        """ Apply a coupon to the cart """
        coupon_code = request.data.get('coupon_code')

        try:
            coupon = Coupon.objects.get(
                code__iexact=coupon_code,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now()
            )
        except Coupon.DoesNotExist:
            return Response(
                {'error': 'Invalid or expired coupon code'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = Cart(request)
        cart.session['coupon_id'] = coupon.id
        cart.save()
        serializer = CartSerializer(cart)

        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def clear(self, request):
        """ Clear the current cart """
        cart = Cart(request)
        cart.clear()

        return Response(
            {'status': 'Cart cleared'},
            status=status.HTTP_204_NO_CONTENT
        )
