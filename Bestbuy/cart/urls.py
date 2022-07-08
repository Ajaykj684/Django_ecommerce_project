from django.urls import path
from . import views


urlpatterns = [



    #cart management
    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('delete_cart/<int:id>/',views.delete_cart,name='delete_cart'),
    path('delete_cart_product/<int:id>/',views.delete_cart_product,name='delete_cart_product'),
    path('review_cart',views.review_cart,name='review_cart'),
    path('update_cart',views.update_cart,name='update_cart'),

    path('update_add_cart',views.update_add_cart,name='update_add_cart'),
    path('update_sub_cart',views.update_sub_cart,name='update_sub_cart'),



    #checkout
    path('buy_now/<int:id>',views.buy_now ,name='buy_now'),

    #wallet
    path('wallet_apply',views.wallet_apply,name='wallet_apply'),

 

]