from django.contrib import admin
from .models import Order,Payment,Order_Product

# Register your models here.

admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(Order_Product)


