
from unicodedata import category
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.shortcuts import  redirect, render,get_object_or_404
from accounts.models import Wallet
from store.models import Product
from . models import Carts, CartItem,Coupon
from django.contrib import auth,messages
from django.db.models import Q

# Create your views here.


def _cart_id(request):
    carts = request.session.session_key
    if not carts:
        carts = request.session.create()
    return carts

def add_cart(request,product_id):
    
    product = Product.objects.get(id=product_id)
    current =request.session.session_key
    try:
        print("yes")
        carts = Carts.objects.get(carts_id = _cart_id(request))
        print(carts)
    except Carts.DoesNotExist:
        print("no")
        if request.user.is_authenticated: 
            carts = Carts.objects.create(
                
                carts_id = _cart_id(request),
                
                user = request.user.email
            )
        else:
            carts = Carts.objects.create(
                
                carts_id = _cart_id(request),
            )

        print("no")
        print(carts)
    carts.save()
    print(carts)
    print("carts")
    print(carts.id)
    
    

    # if Carts.objects.filter(user = request.user).exists():
    #     c = Carts.objects.get(user = request.user , carts_id = current )
    #     carrtt = Carts.objects.filter(user = request.user)
    #     for cart in carrtt:
    #         if cart != c:
    #             if CartItem.objects.filter(cart = cart).exists():
    #                 item =  CartItem.objects.filter(cart = cart)
    #                 for itm in item:
    #                     # new =CartItem.objects.filter(cart = cart)
    #                     new =item.cart_id
    #                 item.update(new = current )
    #                 cart.delete()
    #             else:
    #                 pass
    #         else:
    #             pass
    

    print(cart, "666666655555")
    if request.user.is_authenticated: 

        try :
            cart_item = CartItem.objects.get(product=product , user = request.user)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity = 1,
                cart = carts,
                user = request.user,
            )
            cart_item.save()
        if CartItem.objects.filter(user = request.user).exists():
            item =  CartItem.objects.filter(user = request.user)
            item.update(cart = carts.id)
            if Carts.objects.filter(carts_id = current, user= request.user).exists():
                CC =Carts.objects.get(carts_id = current, user= request.user)
                print(CC)
                print("++++++++++++++++++++")
                
                
            
            if Carts.objects.filter( user= request.user  ).exclude(carts_id = current).exists():
                CC = Carts.objects.filter( user= request.user  ).exclude(carts_id = current)
                print("*********")
                CC.delete()
            pass

    else :
        try :
            
            cart_item = CartItem.objects.get(product=product,cart = carts )
            
            cart_item.quantity += 1
            cart_item.save()
            print("hello")
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity = 1,
                cart = carts,
            )
            cart_item.save()
            print("1")
        

    return redirect('cart')

def update_cart(request):
    print('im here')
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if CartItem.objects.filter(user=request.user , product_id = prod_id ):
            prod_qty = int(request.POST.get('quantity'))
            cart = CartItem.objects.get(product_id = prod_id , user = request.user)
            cart.quantity = prod_qty
            cart.save()
            return JsonResponse({ 'status': "Updated Successfully"})
def cart(request):
    if request.user.is_authenticated:
        
        cart_items = CartItem.objects.filter(user=request.user).order_by('product')
        # cart_count = CartItem.objects.filter(user=request.user,is_active=True).count()
        print(cart_items.count())
        context = {
            'cart_items' : cart_items,
        }
        return render(request,'store/cart.html',context)
    else : 

        try: 
            carts = Carts.objects.get(carts_id = _cart_id(request))
            print(carts)
            
            carts.save()

            cart_items = CartItem.objects.filter( cart = carts)
            print("haiii")
            context = {
                'cart_items' : cart_items,
             }
            return render(request,'store/cart.html',context)
        except:
            print("im here")
            pass
        return render(request,'store/cart.html')
 

def delete_cart(request,id):
    
    cart_item = CartItem.objects.get(id=id,user=request.user)
    
    if request.user.is_authenticated:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart')
    else:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        


def delete_cart_product(request,id):
    
    
    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(id=id,user=request.user)

        cart_item.delete()
        return redirect('cart')
    else:
        carts = Carts.objects.get(carts_id = _cart_id(request))

        cart_item = CartItem.objects.filter(id=id,  cart = carts)
        cart_item.delete()
        return redirect('cart')

def review_cart(request):
    if request.user.is_authenticated:
        final_price = 0
        carrt = Carts.objects.filter(user = request.user)
        carrt.final_offer_price = 0
        cart_items = CartItem.objects.filter(user = request.user)
        for cart_item in cart_items :
            total = (cart_item.product.offer_price * cart_item.quantity)
            final_price = final_price + total
        print(final_price)
        carrt.update(final_offer_price = final_price)
        if Wallet.objects.filter(user = request.user).exists():
            wallet = Wallet.objects.get(user = request.user)
        else:
            wallet = "0"
            
        
        if request.method=="POST":
            name = request.POST['coupon']
            if len(name) == 0 :
                name="none" 
            cart_offer = Carts.objects.filter(carts_id = _cart_id(request))
            
            if Coupon.objects.filter(coupon_code = name, active=True).exists():
                user = request.user
                coupon = Coupon.objects.get(coupon_code = name)
                offer = coupon.discount
                if final_price > 1500 : 
                    price = final_price - (final_price*offer / 100)
                    print(final_price)
                    cartitem = cart_offer.update(coupon_applied=offer, final_offer_price = price, user=user.email )
                    print(offer)
                
                    messages.success(request,'Coupon Added Succesfully')
                else: 
                    messages.error(request,'Sorry   , Coupon Applicable Only for Order above 1500 ')


                context ={ 
                    'offer' : offer,
                    'final_price':final_price,
                    'cart_items': cart_items,
                }
                return render(request,'cart/review_cart.html',context)
            else:
                messages.error(request,'No Coupon Available')
                
                context = {
                    
                    'final_price':final_price,
                    'cart_items': cart_items,
                }
                return render(request,'cart/review_cart.html',context)

        else:
            
            context = {
                
                'final_price':final_price,
                'cart_items': cart_items,
                'wallet' : wallet
            }
            return render(request,'cart/review_cart.html',context)


    else:
        messages.error(request,'you need to Login !')
        try:
            cart = Carts.objects.get(carts_id = _cart_id(request))
            
            print(cart)
            return render(request,'accounts/login.html',{'cart':cart})
        except:
            print("omg")
            
            return render(request,'accounts/login.html')


@login_required()
def buy_now(request,id):
    val = request.POST.get("radio_size")
    user = request.user
    if CartItem.objects.filter(user=user).exists:
        items = CartItem.objects.filter(user=user)

        for item in items:
            item.delete()
    
    product_id = id
    product = Product.objects.get(id=product_id)
    try:
       
        carts = Carts.objects.get(carts_id = _cart_id(request))
    except Carts.DoesNotExist:
       
        carts = Carts.objects.create(
           
            carts_id = _cart_id(request)
        ) 
    
    carts.save()

    if request.user.is_authenticated:
       
        if CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity = 1,
                cart = carts,
                user = request.user,
                size = val,
                
            )
            cart_item.save()

        return redirect('review_cart')

    else : 

        messages.error(request,'you need to Login !')
        return redirect('login')
 

def wallet_apply(request):
    pass
        
         

