from django import forms
from .models import Product

#form for product management
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields= ['product_name','description','price','image1','image2','image3','stock','category','Is_available',]

        