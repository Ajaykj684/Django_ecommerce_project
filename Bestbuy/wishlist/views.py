from email.mime import message
from pyexpat.errors import messages
from django.shortcuts import render,HttpResponse,redirect
from .models import WishlistItem,Wishlist
from store.models import Product

# Create your views here.
def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist


def add_wishlist(request,id):

    product = Product.objects.get(id=id)
    try:
       
        wishlist =  Wishlist.objects.get(wishlist_id = _wishlist_id(request))
    except Wishlist.DoesNotExist:
       
        wishlist = Wishlist.objects.create(
           
            wishlist_id = _wishlist_id(request)
        ) 
    
    wishlist.save()
    if request.user.is_authenticated:
        try :
            wishlist_item = WishlistItem.objects.get(product=product , user = request.user)
            wishlist_item.save()
        except WishlistItem.DoesNotExist:
            wishlist_item = WishlistItem.objects.create(
                product=product,
                
                wishlist = wishlist,
                user = request.user,
            )
            wishlist_item.save()
 


    return redirect('wishlist')

def wishlist(request):
    if request.user.is_authenticated:
        # if Wishlist.objects.filter(wishlist_id = _wishlist_id(request)).exists():
            # wishlist = Wishlist.objects.filter(wishlist_id = _wishlist_id(request))
        wishlistitem = WishlistItem.objects.filter(user = request.user)
        context = { 
                'wishlistitem':wishlistitem
            }
        return render(request,'wishlist/wishlist.html',context)
    else :
        
        return render(request,'wishlist/wishlist.html')

def wishlist_remove(request,id):
    product = Product.objects.get(id = id )
    wishlist_item = WishlistItem.objects.filter(product=product , user = request.user)
    wishlist_item.delete()
    return redirect('wishlist')






