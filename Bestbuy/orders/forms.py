from django import forms
from . models import Order

class Orderform(forms.ModelForm):
    class Meta:
        model = Order
        fields= ['first_name','last_name','phone_number','email','country','state','town','house','zip','order_note',]
