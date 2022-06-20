from django.contrib import admin
from .models import Product

# Register your models here.

# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('product_name','stock','category','modified_date','Is_available')
#     prepopulated_fields = {'slug':('product_name',)}



admin.site.register(Product)
