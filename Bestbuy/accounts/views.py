from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account,Profile, Wallet
from cart.models import CartItem,Carts, Coupon
from django.views.decorators.cache import cache_control
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
import random
from twilio.rest import Client
from django.contrib import messages 
from .decorators import log_out
from bestbuyproject.views import home
from django.conf import settings


# Create your views here.
@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@log_out(home)
def register(request):
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email= form.cleaned_data['email']
            username = email.split("@")[0]
            password = form.cleaned_data['password']
            referel_code = "azdw" + email + last_name + "bcgdj" + first_name + "sdlgqy"
            
            
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password )
            user.save()
            user_name = user
            person = Account.objects.filter(email = user_name)
            person.update( referel_code =referel_code)
            context = { 
                'user_name':user_name
            }
            return render(request,'accounts/phone_number_verify.html',context)
        else:
            messages.error(request,'invalid credentials !')

            form = RegistrationForm()
    form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request,'accounts/register.html',context)


@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@log_out(home)
def login(request):
    id = request.GET.get("id")
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
      

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            if user.is_active == True :
                auth.login(request,user)
            
            if len(id) > 5:

                cartt = Carts.objects.get(carts_id = id)
               
                cart_item = CartItem.objects.filter(cart = cartt )
  
                cart_item.update(user=request.user)
      
            return redirect('/')
        else :
            messages.error(request,'invalid credentials')
            cart = 0
            return redirect('login')  


    
    cart = 0
    return render(request,'accounts/login.html',{'cart':cart})

def login_otp(request):
    if request.method=='POST':
        Phone_no = request.POST['Phone_number']
        Phone_number = "+91" + Phone_no
        if Account.objects.filter(Phone_number = Phone_no).exists():
            user = Account.objects.get(Phone_number = Phone_no)
            account_sid= settings.ACCOUNT_SID
            auth_token= settings.AUTH_TOKEN
            client=Client(account_sid,auth_token)
            verification = client.verify \
                    .services(settings.SERVICES) \
                    .verifications \
                    .create(to=Phone_number,channel='sms')
               
            messages.success(request,'OTP has been sent to 8089224288 & enter OTP')
            return render (request, 'accounts/login_otp1.html',{'Phone_number':Phone_no,'user':user})

        else:
            
            messages.info(request,'invalid mobile number ! !')
            return render (request, 'accounts/login_otp.html')
    return render (request, 'accounts/login_otp.html')

def login_otp1(request,Phone_num):

    if request.method=='POST':
        if Account.objects.filter(Phone_number= Phone_num).exists():
            user = Account.objects.get(Phone_number= Phone_num)
           
            phone_no = "+91" + str(Phone_num)
            otp_input =  request.POST['otp']
         
            if len(otp_input)>0:

                
                account_sid = settings.ACCOUNT_SID
                auth_token = settings.AUTH_TOKEN
                client = Client(account_sid, auth_token)
            
                verification_check = client.verify \
                                    .services(settings.SERVICES) \
                                    .verification_checks \
                                    .create(to= phone_no, code= otp_input)
        
                if verification_check.status == "approved":
                    
                    auth.login(request,user)
                    return redirect('home')
                else:   
                    messages.error(request,'Invalid OTP')
                    return redirect('login_otp1',Phone_num)
            else:
                messages.error(request,'Invalid OTP')
                
                return redirect('login_otp1',Phone_num)

        else:

                messages.error(request,'Invalid Phone number')
                
                return redirect('login_otp1',Phone_num)

    return render(request, 'accounts/login_otp1.html',{'Phone_number':Phone_num})


def logout(request):
    auth.logout(request)
    messages.success(request,'you are logged out !')
    cart =0
    return render(request,'accounts/login.html',{'cart':cart})


def phone_number_verify(request):
    return render(request,'phone_number_verify.html')

def phone_number_verification(request,):
    user_name = request.GET.get('user_name')
    if request.method == 'POST':
        
        count =0
        phone_number = request.POST['Phone_number']
        phone_no = "+91" + phone_number

        for i in phone_number:
            count=count+1
    
        
        if count == 10 :
            if Account.objects.filter(Phone_number=phone_number).exists():
                user1= Account.objects.filter(email = user_name)
                user1.delete()
                messages.info(request,'number already exist ! !')
                return redirect('register')
            else:
                account_sid = settings.ACCOUNT_SID
                auth_token = settings.AUTH_TOKEN
                client=Client(account_sid,auth_token)
                verification = client.verify \
                        .services(settings.SERVICES) \
                        .verifications \
                        .create(to=phone_no,channel='sms')
                messages.success(request,'OTP has been sent to your phone number & enter OTP')
                return render(request,'accounts/phone_verification.html',{'phone_number':phone_number , 'user_name':user_name})

        
        else :  
            if Account.objects.filter(email = user_name).exists():
                user1= Account.objects.filter(email = user_name)
                user1.delete()
                messages.success(request,'entered phone number is not correct !')
                return redirect('register')
           
            else : 
                messages.success(request,'entered phone number is not correct !')
                return redirect('register')

    else : 
            messages.success(request,'Please enter correct phone number !')
            return redirect('register')

def otp_verification(request,Phone_number):
        user_name = request.GET.get('name')
       
        phone_no = "+91" + str(Phone_number)
       
        if request.method == "POST":
            # generated_otp = request.POST['generated_otp']
            otp_input =  request.POST['first']+ request.POST['second']+request.POST['third']+request.POST['fourth']
            account_sid = settings.ACCOUNT_SID
            auth_token = settings.AUTH_TOKEN
            client = Client(account_sid, auth_token)
            
            verification_check = client.verify \
                                    .services(settings.SERVICES) \
                                    .verification_checks \
                                    .create(to= phone_no, code= otp_input)
        
            if verification_check.status == "approved":
                
                user = Account.objects.get(email=user_name)
                user.is_active = True   
                user.Phone_number = Phone_number        
                user.save()          
                auth.login(request,user)          
                try:
                    del request.session['user_mobile']
                    del request.session['user_email']
                except:
                    pass              
              
                return redirect('home')
            else:
                messages.error(request,"Invalid OTP. Try again with correct OTP")
                return render(request,'accounts/phone_verification.html',{'phone_number':Phone_number , 'user_name':user_name})
        else:
            return render(request,'accounts/phone_verification.html',{'phone_number':Phone_number})

@login_required(login_url='login')
def profile(request):
    users = request.user
    countt=0
    wallet = 0
    if Wallet.objects.filter(user = users).exists():
        wallet = Wallet.objects.get(user = users)
    else :
       wall = Wallet.objects.create(user = users)
       wall.save()
      
    if Profile.objects.filter(user = users).exists():
        profile = Profile.objects.filter(user = users)
        countt=0
        
        context = {
            'profile' : profile,
            'countt' : countt,
            'wallet' : wallet
        }
        return render(request,'accounts/profile.html',context)
    else :
        countt=1
        context = {
            
            'countt' : countt,
            'wallet' : wallet
        }
        return render(request,'accounts/profile.html',context)


def Add_address(request):
    user = request.user
   
    if request.method == "POST":
      
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            Phone_number = request.POST['Phone_number']
            
            gender = request.POST['gender']
            house = request.POST['house']
            town = request.POST['town']
            locality = request.POST['locality']
            state = request.POST['state']
            country = request.POST['country']
            zip = request.POST['zip']
            pro=Profile.objects.create(user=user,first_name=first_name,last_name=last_name,Phone_number=Phone_number,gender=gender,house=house,town=town,locality= locality,state=state,country=country,zip=zip)
            pro.save()

            Profile.objects.filter(user = user)
            return redirect('profile')

         
    else:
        return render(request,'accounts/Add_address.html')

def address_delete(request,id):
    if Profile.objects.filter(id=id,user=request.user).exists:
        pro=Profile.objects.get(id=id,user=request.user)
        pro.delete()
        return redirect('profile')

    else:
        return redirect('profile')



def change_password(request):
    user = request.user
    userr = Account.objects.get(email = user)
    if request.method == "POST":
        old_pass = request.POST.get('old_password')
        new_pass = request.POST.get('new_password')
        confirm_pass = request.POST.get('confirm_password')
        
        passw = userr.check_password(old_pass)
        if new_pass == confirm_pass :
            if passw:
                userr.set_password(new_pass)
                userr.save()
                messages.success(request,"password changed Succesfully !")
                return redirect('profile')

            else:
                messages.error(request,"password doesnt exist !")
                return redirect('change_password')
        else:
                messages.error(request,"password doesnt match !")
                return redirect('change_password')

    return render(request,'accounts/change_password.html')


def coupons(request):
    coupons = Coupon.objects.filter(active = True)
    context = {
        'coupons':coupons
    }
    return render(request,'accounts/coupons.html', context)



def referel_add(request):
    user = request.user
    cod = request.POST['code']
    if user.referel_code != cod :

        if Account.objects.filter(referel_code = cod).exists():
            usr = Account.objects.filter(referel_code = cod)
            use = Wallet.objects.get(user = user)
            wall = use.balance + 500
            
            userr = Wallet.objects.filter(user = user)
            userr.update(balance = wall)
            A  = Account.objects.filter(email = user)
            A.update(referel_activated = True)
            messages.success(request,"Referel Successfull. 500 /-  Added to your Wallet, Happy Shopping !")
            return redirect('profile') 
        else:
        
            messages.error(request,"Referel code is wrong !")
            return redirect('profile') 
    else:
        messages.error(request,"Referel code is wrong !")
        return redirect('profile') 
        