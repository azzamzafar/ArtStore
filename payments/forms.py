from django import forms

class SignatureVerificationForm(forms.Form):

    razorpay_order_id = forms.CharField()
    razorpay_payment_id = forms.CharField()
    razorpay_signature = forms.CharField()
    def __init__(self,order_id=None,payment_id=None,signature=None):
        self.razorpay_order_id=order_id
        self.razorpay_payment_id = payment_id
        self.razorpay_signature = signature