from django import forms
from .models import Order
from localflavor.us.forms import USZipCodeField


class OrderCreateForm(forms.ModelForm):
    """ Allows user to create an order """
    postal_code = USZipCodeField()

    class Meta:
        """ metadata """
        model = Order
        fields = [
            'first_name',
            'last_name',
            'email',
            'address',
            'postal_code',
            'city'
        ]
