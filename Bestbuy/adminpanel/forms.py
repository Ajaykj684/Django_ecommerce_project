from django import forms
from category.models import banner

#form for product management
class BannerForm(forms.ModelForm):

    class Meta:
        model = banner

        fields= ['banner_image']

        