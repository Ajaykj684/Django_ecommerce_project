from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def store(request, category_slug=None):
    categories = None
    product =None
    

    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        product = Product.objects.filter(category=categories,Is_available=True)
        product_count = product.count()
    else:
        
        product = Product.objects.all().filter(Is_available=True)
        product_count = product.count()
    
    
    p  = Paginator(product, 6)
    page_num  = request.GET.get('page')
    try:
        page        = p.page (page_num)
    except PageNotAnInteger:
        page        = p.page(1)

    context = {
         'products': page,
         'product_count':product_count,
     }
    return render(request, 'store/store.html',context)

def product_page(request, category_slug, product_slug):
    
    try :
        single_product = Product.objects.get(category__slug= category_slug, slug=product_slug)
    except Exception as e:
        raise e 
    context = {
        'single_product': single_product,
    }

    return render(request,'store/product_page.html',context)