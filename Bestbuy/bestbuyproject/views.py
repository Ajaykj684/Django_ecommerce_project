from django.shortcuts import render
from store.models import Product
from category.models import banner
from cart.models import CartItem
from adminpanel.models import Category_Offer
from .settings import MEDIA_ROOT
from category.models import banner


def home(request):
    products = Product.objects.all().filter(Is_available=True)
    cat_offer = Category_Offer.objects.all()
    
    for cat in cat_offer:
        for product in products: 
            if product.category == cat.category and product.product_offer >=  0 and cat.discount >= 0 and cat.discount <= product.product_offer :
                off =  product.product_offer 
                if off <70 and off > 0 :
                    
                    product.offer_price = product.price-(product.price*off/100)
                    product.offer_perc = product.product_offer
                    product.save()
                else: pass
            elif  product.category == cat.category and product.product_offer >= 0  and cat.discount >= 0  and cat.discount >= product.product_offer :
                if cat.discount < 70 and cat.discount > 0 :
                    product.offer_price = product.price-(product.price*cat.discount/100)

                    product.offer_perc = cat.discount
                    product.save()
            elif product.category != cat.category and product.product_offer > 0 :
                if product.product_offer > 0 and product.product_offer < 70 :
                    product.offer_price = product.price-(product.price*product.product_offer/100)
                    product.save()
            else:
                pass
    

                
    banners = banner.objects.filter(is_selected =True).order_by('id')
    user = request.user
    if user.is_active == True:
        cart_count = CartItem.objects.filter(user=request.user,is_active=True).count()
    else:
        cart_count = 0

    print(cart_count)
    print(banners)
    


    context = {

        
        'cat_offer':cat_offer,
        'products': products,
        'banners':banners,
        'cart_count':cart_count,

    }
    print(MEDIA_ROOT)
    return render(request,'home.html',context)





    # for cat in cat_offer:
    #     for product in products: 
    #         if product.category == cat.category and product.product_offer > 0 :
    #             off = cat.discount + product.product_offer 
    #             if off <100 and off > 0 :
    #                 product.offer_price = product.price-(product.price*off/100)
    #                 product.offer_perc = cat.discount
    #                 product.save()
    #             else: pass
    #         elif product.category == cat.category and product.product_offer <= 0 :
    #             if cat.discount < 100 and cat.discount > 0 :
    #                 product.offer_price = product.price-(product.price*cat.discount/100)

    #                 product.offer_perc = cat.discount
    #                 product.save()
    #         elif product.category != cat.category and product.product_offer > 0 :
    #             if product.product_offer > 0 and product.product_offer < 100 :
    #                 product.offer_price = product.price-(product.price*product.product_offer/100)
    #                 product.save()
    #         else:
    #             pass