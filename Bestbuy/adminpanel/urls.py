from django.urls import path
from . import views

urlpatterns = [ 
     path('',views.login_admin,name='login_admin'),
     path('home_admin',views.home_admin,name='home_admin'),
     path('users_list',views.users_list,name='users_list'),
     path('category_list',views.category_list,name='category_list'),
     path('logout_admin',views.logout_admin,name='logout_admin'),
     path('block_unblock/<int:id>',views.block_unblock,name='block_unblock'),
     path('product_list',views.product_list,name='product_list'),
     path('product_edit/<int:id>',views.product_edit,name='product_edit'),
     path('product_delete/<int:id>',views.product_delete,name='product_delete'),
     path('product_add',views.product_add,name='product_add'),
     path('category_add_page',views.category_add_page,name='category_add_page'),

     path('category_delete/<int:id>',views.category_delete,name='category_delete'),
     path('orders_list',views.orders_list,name='orders_list'),
     path('admin_order_edit/<int:id>/<str:val>',views.admin_order_edit,name='admin_order_edit'),
     path('add_edit_catoffer/<int:id>',views.add_edit_catoffer,name='add_edit_catoffer'),

     path('coupon_list',views.coupon_list,name='coupon_list'),
     path('coupon_disable/<int:id>',views.coupon_disable,name='coupon_disable'),
     path('coupon_edit/<int:id>',views.coupon_edit,name='coupon_edit'),
     path('coupon_add',views.coupon_add,name='coupon_add'),
     
     
     path('sales_report',views.sales_report,name='sales_report'),
     path('offer_management',views.offer_management,name='offer_management'),
     path('category_offer',views.category_offer,name='category_offer'),
     path('category_offer_disable/<int:id>',views.category_offer_disable,name='category_offer_disable'),

     path('product_offer',views.product_offer,name='product_offer'),
     path('product_offer_disable/<int:id>',views.product_offer_disable,name='product_offer_disable'),
     path('product_offer_edit/<int:id>',views.product_offer_edit,name='product_offer_edit'),



     path('export_csv',views.export_csv,name='export_csv'),
     path('export_excel',views.export_excel,name='export_excel'),
     path('export_pdf',views.export_pdf,name='export_pdf'),
     path('show_result',views.show_result,name='show_result'),
     path('monthly_report/<int:date>',views.monthly_report,name='monthly_report'),
     path('yearly_report/<int:date>',views.yearly_report,name='yearly_report'),


     path('todo_list',views.todo_list,name='todo_list'),
     path('todo_delete/<int:id>',views.todo_delete,name='todo_delete'),

     path('banners',views.banners,name='banners'),
     path('banner_select/<int:id>',views.banner_select,name='banner_select'),
     path('add_banner',views.add_banner,name='add_banner'),
     path('remove_banner/<int:id>',views.remove_banner,name='remove_banner'),








    














    
    
   
]