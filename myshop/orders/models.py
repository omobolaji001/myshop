from django.db import models
from django.conf import settings
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from django.utils.translation import gettext as _


class Order(models.Model):
    """ Order class """
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)
    email = models.EmailField(_('e-mail'))
    address = models.CharField(_('address'), max_length=250)
    postal_code = models.CharField(_('postal code'), max_length=20)
    city = models.CharField(_('city'), max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)
    coupon = models.ForeignKey(
        Coupon,
        related_name='orders',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    discount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        """ metadata """
        ordering = ['-created']
        indexes = [models.Index(fields=['-created']), ]

    def __str__(self):
        """ string representation """
        return f'Order {self.id}'

    def get_total_cost_before_discount(self):
        """ Calculate the total cost be discount is applied """
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        """ Returns the discount price applied """
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))

        return Decimal(0)

    def get_total_cost(self):
        """ Calculate the total cost of the
        order items after discount is applied
        """
        total_cost = self.get_total_cost_before_discount()

        return total_cost - self.get_discount()

    def get_stripe_url(self):
        """ Return stripe url """
        if not self.stripe_id:
            # no payment associated
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            # Stripe path for test payments
            path = '/test/'
        else:
            # stripe path for real payments
            path = '/'

        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'


class OrderItem(models.Model):
    """ Represents the order item """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        """ String representation """
        return str(self.id)

    def get_cost(self):
        """ Return the cost of the item """
        return self.price * self.quantity
