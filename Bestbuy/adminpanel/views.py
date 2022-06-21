from datetime import datetime
from urllib import response
from django.http import HttpResponse
from django.shortcuts import redirect,render
from django.contrib.auth import authenticate
from django.contrib import auth,messages 
from django.contrib.auth.decorators import login_required
from cart.models import Coupon
from accounts.models import Account
from category.models import Category, banner
from django.views.decorators.cache import cache_control
from store.models import Product
from store.forms import ProductForm
from category.forms import category_form
from .models import Category_Offer, Todo
import os
from orders.models import Order,Order_Product
import csv
import xlwt
import datetime
from .forms import BannerForm

from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum,Count
from django.db.models.functions import TruncDate



@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def login_admin(request): 

    user =request.user
    if not request.user.is_authenticated :
        if request.method == 'POST':
           
            email = request.POST['email']
            password = request.POST['password']
            

            user = auth.authenticate(email=email, password=password)

            if user is not None:
                if user.is_admin:
                    auth.login(request,user)
                    
                    return redirect('home_admin')
                else:
                    messages.error(request,'invalid credentials')
                   
                    return redirect('login_admin')

            else :
                messages.error(request,'invalid credentials')
                return redirect('login_admin')
        else:
            
            return render(request,'admin/login_admin.html')
    else:
        if user.is_admin:

            return redirect('home_admin')
        else :
            messages.error(request,'invalid credentials !')
            return render(request,'admin/login_admin.html')


   


@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='login_admin')
def home_admin(request):
    label = []
    data = []
    
    completed_order = Order.objects.filter(status='Completed').count()
    pending_order = Order.objects.filter(status='New').count()
    accepted_order = Order.objects.filter(status='Accepted').count()
    cancelled_order = Order.objects.filter(status='Cancelled').count()
    returned_order = Order.objects.filter(status='Returned').count()
    order_status_list = []
    order_status_list.append(completed_order)
    order_status_list.append(accepted_order)
    order_status_list.append(pending_order)
    order_status_list.append(cancelled_order)
    order_status_list.append(returned_order)
    order_count = Order.objects.all().count()
    user_count = Account.objects.count()
    revenue=0
    order = Order_Product.objects.all()
    for item in order:
        revenue = revenue + item.product_price
    


    queryset = Product.objects.all()
    print("o")
    print(order_status_list)
    print(data)
    recent_order = Order.objects.all().order_by('-created_at')[:5]
    print(recent_order)
    print("ajay im here")
    todo = Todo.objects.all().order_by('-id')[:5]
           


    for category in queryset:
        label.append(category.product_name)
        data.append(category.price)
    context = {
        'label':label,
        'data':data,
        'order_count':order_count,
        'order_status_list':order_status_list,
        'user_count':user_count,
        'revenue':revenue,
        'recent_order':recent_order,
        'todo':todo,
    }
    print("0101")
    return render(request,'admin/inddex.html',context)

def users_list(request):
    if request.method == 'POST':
        
        search = request.POST["user_search"] 
        context = Account.objects.filter(first_name__icontains = search)
        return render(request,'admin/user_list.html',{'users': context })
      
    context= Account.objects.all()
  
    return render(request,'admin/user_list.html',{'users': context })

def category_list(request):
     context = Category.objects.all()
     return render(request,'admin/category_list.html',{'categories': context })


@login_required(login_url='login_admin')
def logout_admin(request):
    auth.logout(request)
    return redirect('login_admin')


def product_list(request):
    if request.method == 'POST':
        
        search = request.POST["product_search"] 
        context = Product.objects.filter(product_name__icontains = search)
        return render(request,'admin/product_list.html',{'products': context })
  
    context= Product.objects.all()
    return render( request,'admin/product_list.html',{'products':context})

def block_unblock(request,id):
 
    user = Account.objects.get(id = id)
     
    if user.is_active == True:
        user.is_active = False
        user.save()
        return redirect(users_list)

    else:
        user.is_active =True
        user.save()
        return redirect(users_list)

def product_delete(request,id):
    if request.method == "POST":
        product = Product.objects.get(id=id)
        product.delete()
        return redirect('product_list')

def product_edit(request,id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        product_offer = request.POST.get('offer')
       
        if len(product_name)>0:
            print(product_name)
            Product.objects.filter(id=id).update(product_name=product_name)
            
        if len(description)>0:
            Product.objects.filter(id=id).update(description=description)
        if len(price)>0:
            Product.objects.filter(id=id).update(price=price)
        if len(stock)>0:
            Product.objects.filter(id=id).update(stock=stock)
        if len(product_offer)>0:
            Product.objects.filter(id=id).update(product_offer=product_offer)
        
        if len(request.FILES)>0:
            print("111")
            
           
            print("removed")
            product.image1 = request.FILES['image1']
            product.image2 = request.FILES['image2']
            product.image3 = request.FILES['image3']


            product.save()
            print("saved")
            
        messages.success(request,'Product edited successfully')
        return redirect('product_list')
    else:
        return render (request,'admin/product_edit.html',{'product':product})
    


def product_add(request):
  
    form = ProductForm(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        messages.info(request,'Product added successfully')
        return redirect('product_list')
    context = {'form':form}
    return render(request,'admin/product_add.html',context)


def category_add_page(request):
    
    form = category_form(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        messages.info(request,'Category added successfully')
        return redirect('category_list')
    context = {'form':form}
    return render(request,'admin/category_add_page.html',context)


def category_delete(request,id):
    if request.method == 'POST':
        category_item = Category.objects.get(id=id)
        category_item.delete()
        return redirect('category_list')

    

def orders_list(request):
    orders = Order.objects.all()
    
    return render(request,'admin/orders_list.html',{'orders' : orders})

def admin_order_edit(request,id,val):
        print(val)
        order = Order.objects.get(id=id)
        order.status = val
        print(order.status)
        order.save()
        
        return redirect('orders_list')

def add_edit_catoffer(request,id):
    cat_id =id
    val = request.POST.get("offer")
    category = Category.objects.get(id = cat_id)
    if request.method == "POST":
        if Category_Offer.objects.filter(category_id=cat_id).exists():
            offr = Category_Offer.objects.filter(category_id=cat_id)
            offer = request.POST['offers']
            if int(offer) <= 71 and int(offer) >= 0 :
                print(offer)
                category = val
                offr.update(discount = offer)
                
                return redirect('category_offer')
            else :
                messages.error(request,"Offer must be between 0% to 70%")
                offr = Category_Offer.objects.get(category_id=cat_id)
                discount = offr.discount

                return render(request,'admin/add_edit_catoffer.html',{'cat_id':cat_id , 'category':category ,'discount':discount})


        else:
            offer = request.POST['offers']
            print(offer)
            category = val
            offr = Category_Offer.objects.create(category_id=cat_id,category=val,discount = offer)
            offr.save()
            return redirect('category_offer')
    
    if Category_Offer.objects.filter(category_id=cat_id).exists():
        offr = Category_Offer.objects.get(category_id=cat_id)
        discount = offr.discount
      
        return render(request,'admin/add_edit_catoffer.html',{'cat_id':cat_id , 'category':category ,'discount':discount})
    else:
        return render(request,'admin/add_edit_catoffer.html',{'cat_id':cat_id , 'category':category })


def coupon_list(request):
    coupons = Coupon.objects.all()
    context={ 
        'coupons':coupons
    }
    return render(request,'admin/coupon_list.html',context)

def coupon_disable(request,id):
    
    coupon = Coupon.objects.get(id=id)
    print(coupon)
    if coupon.active == True:
        coupons = Coupon.objects.filter(id=id)
        coupons = coupons.update(active = False)
        
        return redirect('coupon_list')
    
    elif coupon.active == False:
         coupons = Coupon.objects.filter(id=id)
         coupons = coupons.update(active = True)
        
         return redirect('coupon_list')

def coupon_edit(request,id):
    coupon_id = id
    if request.method == 'POST':
        if Coupon.objects.filter(id=coupon_id).exists():
            offr = Coupon.objects.filter(id=coupon_id)
            offer = request.POST['discount']
            coupon_code = request.POST['coupon_code'] 
            print(offer)
            
            offr.update(discount = offer, coupon_code = coupon_code)
            
            return redirect('coupon_list')
    else:
        coupon = Coupon.objects.get(id=coupon_id)
        context = { 
            'coupon_id' : coupon_id,
            'coupon': coupon
        }
        return render(request,'admin/coupon_edit.html',context)

def coupon_add(request):
    if request.method == 'POST':
       
        offer = request.POST.get('discount')
        coupon_code = request.POST.get('coupon_code') 
        print(offer)
            
        coupon = Coupon.objects.create(discount = offer, coupon_code = coupon_code)
        coupon.save() 
        return redirect('coupon_list')
    else : 
        return render(request,'admin/coupon_add.html')

def export_csv(request):

    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachement; filename=SalesReport' +str(datetime.datetime.now())+'.csv'


    writer = csv.writer(response)
    writer.writerow(['order ','name ','amount  ','date'])

    salesreport = Order.objects.all()

    for order in salesreport:
        writer.writerow([order.order_number , order.first_name , order.order_total  , order.created_at ])
    return response

def export_excel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['Content-Disposition'] = 'attachement; filename=SalesReport' +str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet('SalesReport')
    row_num = 0
    font_style =xlwt.XFStyle()
    font_style.font.bold =True

    columns = ['order ','name ','amount  ','date']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num, columns[col_num],font_style)
    
    font_style= xlwt.XFStyle()

    rows = Order.objects.filter(user=request.user).values_list('order_number','first_name','order_total','created_at')

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num,col_num, str(row[col_num]),font_style)

    wb.save(response)

    return response

def export_pdf(request):
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'inline; attachement; filename=SalesReport' +str(datetime.datetime.now())+'.pdf'

    response['Content-Transfer-Encoding'] = 'binary'

    salesreport = Order.objects.all()
    total= salesreport.aggregate(Sum('order_total'))

    html_string = render_to_string('admin/pdf_output.html',{ 'salesreport':salesreport, 'total': total})

    html=HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output : 
        output.write(result)
        output.flush()


        output=open(output.name,'rb')

        response.write(output.read())

    return response


def sales_report(request):
    salesreport = Order.objects.all()
    total = 0
    total= salesreport.aggregate(Sum('order_total'))
    
    context = {
        'salesreport': salesreport ,
        'total':    total

    }
    return render(request,'admin/sales_report.html',context)

def offer_management(request):
    return render(request,'admin/offer_management.html')

def category_offer(request):
    context = Category.objects.all()

    return render(request,'admin/category_offer.html',{'categories': context })

def category_offer_disable(request,id):
    
    cat_off = Category_Offer.objects.get(id=id)
    print(cat_off)
    if cat_off.active == True:
        cat_of = Category_Offer.objects.filter(id=id)
        cat = cat_of.update(active = False)
    elif cat_off.active == False:
        cat_of = Category_Offer.objects.filter(id=id)
        cat = cat_of.update(active = True)
    return redirect('category_offer')


def product_offer(request):
    if request.method == 'POST':
        
        search = request.POST["product_search"] 
        context = Product.objects.filter(product_name__icontains = search)
        return render(request,'admin/product_offer.html',{'products': context })
    context= Product.objects.all().order_by('product_name')
    return render( request,'admin/product_offer.html',{'products':context})
   

def product_offer_disable(request,id):
    product_off = Product.objects.get(id=id)
    print(product_off.Is_offer_active)
    print(product_off)
    if product_off.Is_offer_active == True:
        product_of = Product.objects.filter(id=id)
        print(product_of)
        print("1")
        product_of.update(Is_offer_active = False)
        print(product_off.Is_offer_active)
    elif product_off.Is_offer_active == False:
        print("2")
        product_of = Product.objects.filter(id=id)
        product_of.update(Is_offer_active = True)
        print(product_of)
    return redirect('product_offer')


def product_offer_edit(request,id):
    
    product = Product.objects.get(id=id)
    val = request.POST.get('offer')
    
    if request.method == "POST":
        if Product.objects.filter(id=id).exists():
            offr = Product.objects.filter(id=id)
            offer = request.POST['offers']
            if int(offer) <= 71 and int(offer) >= 0 :
            
                offr.update(product_offer=offer)
                return redirect('product_offer')
            else :
                messages.error(request,"Offer must be between 0% to 70%")
                return render(request,'admin/product_offer_edit.html',{'product':product, 'id':id})

        else:
            return redirect('product_offer')
    else:
        
        return render(request,'admin/product_offer_edit.html',{'product':product, 'id':id})

def todo_list(request):
    Todo_list = Todo.objects.all()
    if request.method == "POST":
        
        todo = request.POST.get('todo')
        Todo_list=Todo.objects.create(todo_list = todo )
        return redirect('home_admin')
    else:
        print("qqq")
        pass

def todo_delete(request,id):
    todo = Todo.objects.filter(id=id)
    todo.delete()
    return redirect('home_admin')


def show_result(request):
    order = Order.objects.all()
    if request.method == "POST":
        fromdate =request.POST.get('fromdate')
        todate =request.POST.get('todate')
        if len(fromdate) > 0 and len(todate) > 0 :
            frm = fromdate.split("-")
            tod = todate.split("-")

            fm = [int(x) for x in frm]
            todt = [int(x) for x in tod]
            print(fm)

                
            salesreport = Order.objects.filter(created_at__gte=datetime.date(fm[0],fm[1],fm[2]), created_at__lte=datetime.date(todt[0],todt[1],todt[2])).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).annotate(sum=Sum('order_total')).order_by('-day')
            
            context = {

                'salesreport' : salesreport ,   

            }
            print(salesreport)
            print("111")
            return render(request,'admin/sales_report_search.html',context)
        else:
            salesreport = Order.objects.all()
            context = {
                'salesreport': salesreport ,

             }
            return render(request,'admin/sales_report.html',context)

    else:
        salesreport = Order.objects.all()
        context = {
            'salesreport': salesreport ,
        

        }
        return render(request,'admin/sales_report.html',context)



def monthly_report(request,date):
    
    frmdate = date
   
    fm = [ 2022 , frmdate , 1 ]
    todt = [2022 , frmdate , 28 ]
    
    print(fm)
            
    salesreport = Order.objects.filter(created_at__gte=datetime.date(fm[0],fm[1],fm[2]), created_at__lte=datetime.date(todt[0],todt[1],todt[2])).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).annotate(sum=Sum('order_total')).order_by('-day')
    if len(salesreport) > 0 :   
        context = {
                'salesreport' : salesreport ,   
            }
        print(salesreport)
        print("111")
        return render(request,'admin/sales_report_search.html',context)
    else:
        messages.error(request,"No Orders")
        return render(request,'admin/sales_report_search.html')
    

def yearly_report(request,date):
   
    frmdate = date
   
    fm = [ frmdate , 1 , 1 ]
    todt = [frmdate , 12 , 30 ]
    
    print(fm)
            
    salesreport = Order.objects.filter(created_at__gte=datetime.date(fm[0],fm[1],fm[2]), created_at__lte=datetime.date(todt[0],todt[1],todt[2])).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).annotate(sum=Sum('order_total')).order_by('-day')
    if len(salesreport) > 0 :   
        context = {
                'salesreport' : salesreport ,   
            }
        print(salesreport)
        print("111")
        return render(request,'admin/sales_report_search.html',context)
    else:
        messages.error(request,"No Orders")
        return render(request,'admin/sales_report_search.html')




def banners(request):
    bannr = banner.objects.all()
    return render(request,'admin/banner.html',{'bannr':bannr})

def banner_select(request,id):
    bannr = banner.objects.all()
    bannr.update(is_selected = False )
    banners = banner.objects.filter(id = id)
    banners.update(is_selected = True)
    return redirect('banners')

def add_banner(request):
    form = BannerForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():

            form.save()
            return redirect('banners')
    else:
        context = {'form':form}
        return render(request,'admin/add_banner.html',context)

def remove_banner(request , id):
    bannr = banner.objects.filter(id= id)
    bannr.delete()
    return redirect(banners)