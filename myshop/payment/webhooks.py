import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from .tasks import payment_completed


@csrf_exempt
def stripe_webhook(request):
    """ Handles Stripe webhook """
    payload = request.body
    sig_header = request.headers.get('stripe-signature')
    event = None

    try:
        event = stripe.Webhook.construct_event(
                    payload, sig_header,
                    settings.STRIPE_WEBHOOK_SECRET
                )
    except ValueError as e:
        # invalid payload
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError as e:
        # invalid signature
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        # print(f'client_reference_id = {session.client_reference_id}')

        if (session.mode == 'payment' and session.payment_status == 'paid'):
            try:
                order = Order.objects.get(id=session.client_reference_id)

                # mark order as paid
                order.paid = True
                order.stripe_id = session.payment_intent
                order.save()

                # launch asynchronous task
                payment_completed.delay(order.id)

            except Order.DoesNotExist:
                print("Order not found")
                return HttpResponse(status=404)

    return HttpResponse(status=200)
