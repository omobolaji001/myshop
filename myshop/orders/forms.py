from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """ Allows user to create an order """
    class Meta:
        """ metadata """
        model = Order
        fields = ['first_name', 'last_name', 'email',
                  'address', 'postal_code', 'city']
