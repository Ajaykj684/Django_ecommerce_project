from django.urls import path
from . import views


urlpatterns = [
    path('wishlist',views.wishlist,name='wishlist'),
    path('add_wishlist/<int:id>',views.add_wishlist,name='add_wishlist'),
    path('wishlist_remove/<int:id>',views.wishlist_remove,name='wishlist_remove'),


   

]