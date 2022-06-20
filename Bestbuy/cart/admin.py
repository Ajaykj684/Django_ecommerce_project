from django.contrib import admin
from . models import Carts, CartItem,Coupon,Paymentrazor,Orderss

# Register your models here.

admin.site.register(Carts)
admin.site.register(CartItem)
admin.site.register(Coupon)
admin.site.register(Paymentrazor)
admin.site.register(Orderss)

