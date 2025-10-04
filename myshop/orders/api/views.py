import stripe
from django.conf import settings
from orders.api.serializers import OrderSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order, OrderItem
from cart.cart import Cart
from shop.models import Product
from decimal import Decimal


class OrderViewSet(viewsets.ViewSet):
    """ Order view set """

    permission_classes = [AllowAny]
    serializer_class = OrderSerializer

    @action(detail=False, methods=['post'])
    def create_order(self, request):
        """ Creates an order from the cart """
        cart = Cart(request)

        if not cart.cart:
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

            # Retrieve order details
            order_data = {
                'first_name': request.data.get('first_name'),
                'last_name': request.data.get('last_name'),
                'email': request.data.get('email'),
                'address': request.data.get('address'),
                'postal_code': request.data.get('postal_code'),
                'city': request.data.get('city'),
                'discount': cart.coupon.discount if cart.coupon else 0,
                'coupon': cart.coupon
            }

            serializer = OrderSerializer(
                data=order_data,
                context={'request': request}
            )
            if serializer.is_valid():
                order = serializer.save()

                # Create order items from cart
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        quantity=item['quantity'],
                        price=item['price']
                    )

                # Clear cart after order creation
                cart.clear()

                # set order in session
                request.session['order_id'] = order.id

                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
