from django import forms


class CouponApplyForm(forms.Form):
    """ Accepts a coupon code """
    code = forms.CharField()
