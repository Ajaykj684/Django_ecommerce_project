from django.urls import path
from . import views

urlpatterns = [ 
    path('confirm_order/',views.confirm_order,name='confirm_order'),

    path('place_order',views.place_order,name='place_order'),
    path('payment_select/<str:order_id>/',views.payment_select,name='payment_select'),
    path('cash_on_delivery/<int:val>',views.cash_on_delivery,name='cash_on_delivery'),
    path('payment_successfull/',views.payment_successfull,name='payment_successfull'),
    path('paypal_success',views.paypal_success,name='paypal_success'),
    path('razorpay_success',views.razorpay_success,name='razorpay_success'),

    path('payment/<int:check>',views.order_payment),
    path("razorpay/callback/", views.callback),
    path("course", views.course_changer, ),



    path('my_orders',views.my_orders,name='my_orders'),
    path('order_view/<int:id>/',views.order_view,name='order_view'),
    path('order_cancel/<int:id>/',views.order_cancel,name='order_cancel'),
    path('order_return/<int:id>/',views.order_return,name='order_return'),
    path('export_invoice_pdf',views.export_invoice_pdf,name='export_invoice_pdf'),

    path('address',views.address,name='address'),


    









]