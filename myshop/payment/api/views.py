import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentViewSet(viewsets.ViewSet):
    """ Handles payment """
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def create_checkout(self, reqeust):
        """ Creates a Stripe checkout session for existing order """
        order_id = request.session.get('order_id')

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if order.paid:
            return Response(
                {'error': 'Order is already paid'},
                status=status.HTTP_400_BAD_REQUEST
            )

        success_url = request.build_absolute_uri('/payment/success/')
        cancel_url = request.build_absolute_uri('/payment/cancel/')
        sesssion_data = {
            'mode': 'payment',
            'client_renference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }

        # add order items to Stripe checkout session
        for item in order.items.all():
            session_data['line_items'].append(
                {'price_data':
                    {'unit_amount': int(item.price * Decimal('100')),
                     'currency': 'usd',
                     'product_data': {'name': item.product.name, },
                    },
                 'quantity': item.quantity,
                }
            )

        try:
            # create Stripe checkout session
            session = stripe.checkout.Session.create(**session_data)
            order.save()

            return Response(
                {
                    'order_id': order.id,
                    'checkout_url': session.url
                },
                status=status.HTTP_200_OK
            )
        except stripe.error.StripeError as e:
            return Response(
                {'error': f'Stripe error: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    @csrf_exempt
    def webhook(self, request):
        """ Handle Stripe webhook events """
        payload = request.body
        sig_header = request.headers.get('stripe-signature')
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header,
                settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)

        if event.type == 'checkout.session.completed':
            session = event.data.object

            if (session.mode == 'payment' and session.payment_status == 'paid'):
                try:
                    order = Order.objects.get(id=session.client_reference_id)
                    order.paid = True
                    order.stripe_id = session.payment_intent
                    order.save()
                except Order.DoesNotExist:
                    return HttpResponse(status=404)

        return HttpResponse(status=200)
