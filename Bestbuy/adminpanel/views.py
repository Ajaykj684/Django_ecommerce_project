from datetime import datetime
from tkinter.ttk import LabeledScale
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
from orders.models import Order,Order_Product, Payment
import csv
import xlwt
import datetime
from .forms import BannerForm
from .decorators import log
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum,Count
from django.db.models.functions import TruncDate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

count = 0


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
                    global count
                    count = 0
                    
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
@log(login_admin)
def home_admin(request):
    global count
    count = count+1
    labal = []
    datas = []
    
    completed_order = Order.objects.filter(status='Delivered').count()
    pending_order = Order.objects.filter(status='Confirmed').count()
    accepted_order = Order.objects.filter(status='Out_for_delivery').count()
    cancelled_order = Order.objects.filter(status='Cancelled').count()
    returned_order = Order.objects.filter(status='Returned').count()
    order_status_list = []
    order_status_list.append(completed_order)
    order_status_list.append(accepted_order)
    order_status_list.append(cancelled_order)
    order_status_list.append(pending_order)
    order_status_list.append(returned_order)
    order_count = Order.objects.all().count()
    user_count = Account.objects.count()
    revenue=0
    order = Order_Product.objects.all()
    for item in order:
        revenue = revenue + item.product_price

    queryset = Product.objects.all()
    recent_order = Order.objects.all().order_by('-created_at')[:5]
    todo = Todo.objects.all().order_by('-id')[:5]
    for prodct in queryset:
        labal.append(prodct.product_name)
        datas.append(prodct.price)
   
    coupons = Coupon.objects.all()[:3]

    context = {
        'labal':labal,
        'datas':datas,
        'order_count':order_count,
        'order_status_list':order_status_list,
        'user_count':user_count,
        'revenue':revenue,
        'recent_order':recent_order,
        'todo':todo,
        'count':count,
        'coupons' :coupons
        
        

       
    }
    return render(request,'admin/inddex.html',context)
    

def product_chart(request):
    
    labels = []
    data = []

    queryset = Product.objects.filter().order_by('product_name')[:8]
    for product in queryset:
        labels.append(product.product_name)
        data.append(product.price)
    print(data , labels)


    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })    


def payment_chart(request):
    
    labels = []
    data = []
    queryst = Payment.objects.all()[:23]


    for prod in queryst :
        labels.append(prod.payment_method)
        data.append(prod.amount_paid)


    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })    



@log(login_admin)
def users_list(request):
    if request.method == 'POST':
        
        search = request.POST["user_search"] 
        context = Account.objects.filter(first_name__icontains = search , is_admin = False )
        return render(request,'admin/user_list.html',{'users': context })
      
    context= Account.objects.filter(is_admin = False)
  
    return render(request,'admin/user_list.html',{'users': context })

def category_list(request):

    if request.method == 'POST':

        search = request.POST["category_search"] 
        context = Category.objects.filter(category_name__icontains = search)
        return render(request,'admin/category_list.html',{'categories': context })
    

    category = Category.objects.all()
    p  = Paginator(category, 5)
    page_num  = request.GET.get('page')
    try:
        page        = p.page (page_num)
    except PageNotAnInteger:
        page        = p.page(1)
    
    return render(request,'admin/category_list.html',{'categories': page })


@login_required(login_url='login_admin')
def logout_admin(request):
    auth.logout(request)
    return redirect('login_admin')

@log(login_admin)
def product_list(request):
    if request.method == 'POST':
        
        search = request.POST["product_search"] 
        context = Product.objects.filter(product_name__icontains = search)
        return render(request,'admin/product_list.html',{'products': context })
  
    product= Product.objects.all()
    p  = Paginator(product, 4)
    page_num  = request.GET.get('page')
    try:
        page        = p.page (page_num)
    except PageNotAnInteger:
        page        = p.page(1)
    return render( request,'admin/product_list.html',{'products':page})


@log(login_admin)
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


@log(login_admin)
def product_delete(request,id):
    if request.method == "POST":
        product = Product.objects.get(id=id)
        product.delete()
        return redirect('product_list')



@log(login_admin)

def product_edit(request, id):
    product_detail = Product.objects.get(id=id)
    if request.method == 'POST':
        if len(request.FILES) != 0: 
            if product_detail.image1:
                
                product_detail.image1       = request.FILES.get('image1')

            if product_detail.image2:
                
                product_detail.image2       = request.FILES.get('image2')

            if product_detail.image3:
                
                product_detail.image3       = request.FILES.get('image3')

        product_detail.product_name     = request.POST.get('product_name')
        product_detail.description      = request.POST.get('description')
        product_detail.price            = request.POST.get('price')
        product_detail.stock            = request.POST.get('stock')
        if product_detail.price < "0" or product_detail.stock  < "0":
            messages.error(request, 'Please Fill with correct Value')
            return redirect(product_edit,id)

        product_detail.save()  
        return redirect(product_list)
       

    product     = Product.objects.get(id=id)
    category       = Category.objects.all()
    return render(request, 'admin/product_edit.html', {'product': product, 'category': category} )

    




def product_add(request):
    product = Product()
    cate = Category.objects.all()
    if request.method == "POST":

        product.product_name        = request.POST.get('product_name')
        product.description         = request.POST.get('description')
        product.price               = request.POST.get('price')
        product.stock               = request.POST.get('stock')
        categ                       = request.POST.get('category')
        
        if product.price < "0" or product.stock < "0":
            messages.error(request, 'Please Fill with correct Value')
            return redirect(product_add)
        if len(product.product_name) == 0 or len(categ) == 0:
            messages.error(request, 'Fields cannot be blank')
            return redirect(product_add)

        product.category            = Category.objects.get(id=categ)

        if len(request.FILES) != 0:
            product.image1              = request.FILES.get('image')    
            product.image2          = request.FILES.get('image2')    
            product.image3        = request.FILES.get('image3')    
            product.save()
            
            return redirect('product_list')
        else:
            messages.error(request, "Please insert an image ")
            
            return render(request,'admin/product_add.html',{'cate': cate},)
        
        
             
    else:
        cate = Category.objects.all()
        return render(request, 'admin/product_add.html', {'cate': cate}, )




@log(login_admin)
def category_add_page(request):
    
    form = category_form(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        messages.info(request,'Category added successfully')
        return redirect('category_list')
    context = {'form':form}
    return render(request,'admin/category_add_page.html',context)



@log(login_admin)
def category_delete(request,id):
    if request.method == 'POST':
        category_item = Category.objects.get(id=id)
        category_item.delete()
        return redirect('category_list')

    
@log(login_admin)
def orders_list(request):

    if request.method == 'POST':
        
        search = request.POST["orders_search"] 
        context = Order.objects.filter(first_name__icontains = search)
        return render(request,'admin/orders_list.html',{'orders': context })
    orders = Order.objects.all()
    p  = Paginator(orders, 8)
    page_num  = request.GET.get('page')
    try:
        page        = p.page (page_num)
    except PageNotAnInteger:
        page        = p.page(1)
    
    return render(request,'admin/orders_list.html',{'orders' : page})


@log(login_admin)
def admin_order_edit(request,id,val):
        order = Order.objects.get(id=id)
        order.status = val
        order.save()
        
        return redirect('orders_list')


@log(login_admin)
def add_edit_catoffer(request,id):
    cat_id =id
    val = request.POST.get("offer")
    category = Category.objects.get(id = cat_id)
    if request.method == "POST":
        if Category_Offer.objects.filter(category_id=cat_id).exists():
            offr = Category_Offer.objects.filter(category_id=cat_id)
            offer = request.POST['offers']
            if len(offer) == 0:
                offer = 0
            if int(offer) <= 71 and int(offer) >= 0 :
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




@log(login_admin)
def coupon_list(request):
    coupons = Coupon.objects.all()
    context={ 
        'coupons':coupons
    }
    return render(request,'admin/coupon_list.html',context)



@log(login_admin)
def coupon_disable(request,id):
    
    coupon = Coupon.objects.get(id=id)
    if coupon.active == True:
        coupons = Coupon.objects.filter(id=id)
        coupons = coupons.update(active = False)
        
        return redirect('coupon_list')
    
    elif coupon.active == False:
         coupons = Coupon.objects.filter(id=id)
         coupons = coupons.update(active = True)
        
         return redirect('coupon_list')



@log(login_admin)
def coupon_edit(request,id):
    coupon_id = id
    if request.method == 'POST':
        if Coupon.objects.filter(id=coupon_id).exists():
            offr = Coupon.objects.filter(id=coupon_id)
            offer = request.POST['discount']
            coupon_code = request.POST['coupon_code'] 
            
            offr.update(discount = offer, coupon_code = coupon_code)
            
            return redirect('coupon_list')
    else:
        coupon = Coupon.objects.get(id=coupon_id)
        context = { 
            'coupon_id' : coupon_id,
            'coupon': coupon
        }
        return render(request,'admin/coupon_edit.html',context)


@log(login_admin)
def coupon_add(request):
    if request.method == 'POST':
       
        offer = request.POST.get('discount')
        coupon_code = request.POST.get('coupon_code') 
            
        coupon = Coupon.objects.create(discount = offer, coupon_code = coupon_code)
        coupon.save() 
        return redirect('coupon_list')
    else : 
        return render(request,'admin/coupon_add.html')



@log(login_admin)
def export_csv(request):

    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachement; filename=SalesReport' +str(datetime.datetime.now())+'.csv'


    writer = csv.writer(response)
    writer.writerow(['order ','name ','amount  ','date'])

    salesreport = Order.objects.all()

    for order in salesreport:
        writer.writerow([order.order_number , order.first_name , order.order_total  , order.created_at ])
    return response


@log(login_admin)
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



@log(login_admin)
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



@log(login_admin)
def sales_report(request):
    salesreport = Order.objects.all()
    total = 0
    total= salesreport.aggregate(Sum('order_total'))

    if request.method == 'POST':
        
        search = request.POST["salesreport_search"] 
        salesreports = Order.objects.filter(order_number__icontains = search)
       
        context = {
            'salesreport': salesreports ,
            'total':    total
        }
        return render(request,'admin/sales_report.html',context)
    p  = Paginator(salesreport, 10)
    page_num  = request.GET.get('page')
    try:
        page        = p.page (page_num)
    except PageNotAnInteger:
        page        = p.page(1)
    
    
    context = {
        'salesreport': page ,
        'total':    total

    }
    return render(request,'admin/sales_report.html',context)



@log(login_admin)
def offer_management(request):
    return render(request,'admin/offer_management.html')



@log(login_admin)
def category_offer(request):
    context = Category.objects.all()

    return render(request,'admin/category_offer.html',{'categories': context })



@log(login_admin)
def category_offer_disable(request,id):
    
    cat_off = Category_Offer.objects.get(id=id)
    if cat_off.active == True:
        cat_of = Category_Offer.objects.filter(id=id)
        cat_of.update(active = False, discount=0)
    elif cat_off.active == False:
        cat_of = Category_Offer.objects.filter(id=id)
        cat = cat_of.update(active = True,discount=0)
    return redirect('category_offer')



@log(login_admin)
def product_offer(request):
    if request.method == 'POST':
        
        search = request.POST["product_search"] 
        context = Product.objects.filter(product_name__icontains = search)
        return render(request,'admin/product_offer.html',{'products': context })
    context= Product.objects.all().order_by('product_name')
    return render( request,'admin/product_offer.html',{'products':context})
   


@log(login_admin)
def product_offer_disable(request,id):
    product_off = Product.objects.get(id=id)
   
    if product_off.Is_offer_active == True:
        product_of = Product.objects.filter(id=id)
     
        product_of.update(Is_offer_active = False, product_offer = 0)
    elif product_off.Is_offer_active == False:
        product_of = Product.objects.filter(id=id)
        product_of.update(Is_offer_active = True, product_offer = 0)
    return redirect('product_offer')



@log(login_admin)
def product_offer_edit(request,id):
    
    product = Product.objects.get(id=id)
    val = request.POST.get('offer')
    
    if request.method == "POST":
        if Product.objects.filter(id=id).exists():
            offr = Product.objects.filter(id=id)
            offer = request.POST['offers']
            if len(offer) == 0:
                offer = 0
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


@log(login_admin)
def todo_list(request):
    Todo_list = Todo.objects.all()
    if request.method == "POST":
        
        todo = request.POST.get('todo')
        Todo_list=Todo.objects.create(todo_list = todo )
        return redirect('home_admin')
    else:
        pass


@log(login_admin)
def todo_delete(request,id):
    todo = Todo.objects.filter(id=id)
    todo.delete()
    return redirect('home_admin')


@log(login_admin)
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
                
            salesreport = Order.objects.filter(created_at__gte=datetime.date(fm[0],fm[1],fm[2]), created_at__lte=datetime.date(todt[0],todt[1],todt[2])).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).annotate(sum=Sum('order_total')).order_by('-day')
            
            context = {

                'salesreport' : salesreport ,   

            }
          
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




@log(login_admin)
def monthly_report(request,date):
    
    frmdate = date
   
    fm = [ 2022 , frmdate , 1 ]
    todt = [2022 , frmdate , 28 ]
    
    salesreport = Order.objects.filter(created_at__gte=datetime.date(fm[0],fm[1],fm[2]), created_at__lte=datetime.date(todt[0],todt[1],todt[2])).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).annotate(sum=Sum('order_total')).order_by('-day')
    if len(salesreport) > 0 :   
        context = {
                'salesreport' : salesreport ,   
            }
 
        return render(request,'admin/sales_report_search.html',context)
    else:
        messages.error(request,"No Orders")
        return render(request,'admin/sales_report_search.html')
    



@log(login_admin)
def yearly_report(request,date):
   
    frmdate = date
   
    fm = [ frmdate , 1 , 1 ]
    todt = [frmdate , 12 , 30 ]

    salesreport = Order.objects.filter(created_at__gte=datetime.date(fm[0],fm[1],fm[2]), created_at__lte=datetime.date(todt[0],todt[1],todt[2])).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).annotate(sum=Sum('order_total')).order_by('-day')
    if len(salesreport) > 0 :   
        context = {
                'salesreport' : salesreport ,   
            }
  
        return render(request,'admin/sales_report_search.html',context)
    else:
        messages.error(request,"No Orders")
        return render(request,'admin/sales_report_search.html')



@log(login_admin)
def banners(request):
    bannr = banner.objects.all()
    return render(request,'admin/banner.html',{'bannr':bannr})



@log(login_admin)
def banner_select(request,id):
    bannr = banner.objects.all()
    bannr.update(is_selected = False )
    banners = banner.objects.filter(id = id)
    banners.update(is_selected = True)
    return redirect('banners')



@log(login_admin)
def add_banner(request):
    form = BannerForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():

            form.save()
            return redirect('banners')
    else:
        context = {'form':form}
        return render(request,'admin/add_banner.html',context)



@log(login_admin)
def remove_banner(request , id):
    bannr = banner.objects.filter(id= id)
    bannr.delete()
    return redirect(banners)

@log(login_admin)
def view_order(request,id):
    order = Order.objects.get(id = id)
    order_prod = Order_Product.objects.filter(order = order)
    return render(request,"admin/view_order.html",{"order_prod":order_prod , "orders":order})



