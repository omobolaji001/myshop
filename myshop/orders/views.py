from django.shortcuts import render, redirect
from .forms import OrderCreateForm
from .models import OrderItem
from .tasks import order_created
from cart.cart import Cart


def order_create(request):
    """ Handles order creation """
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
        cart.clear()

        # launch asynchronous task
        order_created.delay(order.id)

        # set order in the session
        request.session['order_id'] = order.id

        # redirect for payment
        return redirect('payment:process')

    else:
        form = OrderCreateForm()
        return render(
            request, 'orders/order/create.html',
            {'cart': cart, 'form': form}
        )
