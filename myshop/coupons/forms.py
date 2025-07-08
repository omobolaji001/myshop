from django import forms
from django.utils.translation import gettext_lazy as _


class CouponApplyForm(forms.Form):
    """ Accepts a coupon code """
    code = forms.CharField(label=_('Coupon'))
