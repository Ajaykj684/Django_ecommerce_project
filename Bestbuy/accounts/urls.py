from django.urls import path
from . import views

urlpatterns = [ 
     path('register/',views.register,name='register'),
     path('login/',views.login,name='login'),
     path('logout/',views.logout,name='logout'), 
     path('login_otp/', views.login_otp, name='login_otp'),
     path('login_otp1/', views.login_otp1, name='login_otp1'),
     path('phone_number_verification/', views.phone_number_verification, name='phone_number_verification'),
     path('phone_number_verify/', views.phone_number_verify, name='phone_number_verify'),

     path('otp_verification/<int:Phone_number>/', views.otp_verification, name='otp_verification'),
     path('profile/', views.profile, name='profile'),

     path('coupons/', views.coupons, name='coupons'),

     path('Add_address/', views.Add_address, name='Add_address'),
     path('address_delete/<int:id>/', views.address_delete, name='address_delete'),

     path('change_password', views.change_password, name='change_password'),

     path('referel_add/', views.referel_add, name='referel_add'),

   
   
]