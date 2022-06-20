from .models import Category
from django import forms

class category_form(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = '__all__'