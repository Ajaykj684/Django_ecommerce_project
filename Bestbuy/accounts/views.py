from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account,Profile, Wallet
from cart.models import CartItem,Carts, Coupon

from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
import random
from twilio.rest import Client
from django.contrib import messages 


# Create your views here.


def register(request):
    print("22")
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print("211111111111112")
        
        if form.is_valid():
            print("21888888888888")

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            # Phone_number = form.cleaned_data['Phone_number']
            email= form.cleaned_data['email']
            username = email.split("@")[0]
            password = form.cleaned_data['password']
            
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            # user.Phone_number = Phone_number
            user.save()
            user_name = user
            context = { 
                'user_name':user_name
            }
            #messages.success(request,'Welcome , Registered Succesfully !')
            return render(request,'accounts/phone_number_verify.html',context)
        else:
            print("uuuuuu")

            messages.error(request,'invalid credentials !')

            form = RegistrationForm()
    form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request,'accounts/register.html',context)

def login(request):
    id = request.GET.get("id")
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
      

        user = auth.authenticate(email=email, password=password)
        print(111111)
        if user is not None:
            auth.login(request,user)
            
            if len(id) > 5:

                cartt = Carts.objects.get(carts_id = id)
               
                cart_item = CartItem.objects.filter(cart = cartt )
                print(cart_item)
                print("loook")
                cart_item.update(user=request.user)
                    
                    
                print("k")
            return redirect('/')
        else :
            print(1)
            messages.error(request,'invalid credentials')
            cart = 0
            return redirect('login')   #,{'cart':cart}


    
    cart = 0
    return render(request,'accounts/login.html',{'cart':cart})

def login_otp(request):
    if request.method=='POST':
        mobile='8089224288'
        Phone_number = request.POST['Phone_number']
        if mobile==Phone_number:
            # Your Account SID twilio
            account_sid = "AC49e8bec60a3167343774d727aad5de8d"
            # Your Auth Token twilio    
            auth_token  = "1f4cc794eb5b3dd3b54603aee566384f"

            client = Client(account_sid, auth_token)
            global otp
            otp = str(random.randint(1000,9999))
            message = client.messages.create(
                to="+918089224288", 
                from_="+12517661906",
                body="Hello there! Your Login OTP is"+otp)
            messages.success(request,'OTP has been sent to 8089224288 & enter OTP')
            return render (request, 'accounts/login_otp1.html')

        else:
            
            messages.info(request,'invalid mobile number ! !')
            return render (request, 'accounts/login_otp.html')
    return render (request, 'accounts/login_otp.html')

def login_otp1(request):
    if request.method=='POST':
        if Account.objects.filter(Phone_number= 8089224288).exists():
            user = Account.objects.get(Phone_number= 8089224288)
            otpvalue = request.POST['otp']
            if len(otpvalue)>0:

                if otpvalue == otp:
                    auth.login(request,user)
                    messages.success(request,'You are logged in')
                    return redirect('/')
                else:   
                    messages.error(request,'Invalid OTP')
                    return redirect('login_otp1')
            else:
                messages.error(request,'Invalid OTP')
                return redirect('login_otp1')
        else:

                messages.error(request,'Invalid Phone number')
                return redirect('login_otp1')

    return render(request, 'accounts/login_otp1.html')

# @login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'you are logged out !')
    cart =0
    return render(request,'accounts/login.html',{'cart':cart})
def phone_number_verify(request):
    return render(request,'phone_number_verify.html')

def phone_number_verification(request,):
    user_name = request.GET.get('user_name')
    print(user_name)
    if request.method == 'POST':
        
        print("1")
        count =0
        phone_number = request.POST['Phone_number']

        for i in phone_number:
            count=count+1
        
        c="+91" + phone_number
        
        
        if count == 10 :
            print("0000")
            if Account.objects.filter(Phone_number=phone_number).exists():
                user1= Account.objects.filter(email = user_name)
                user1.delete()
                messages.info(request,'number already exist ! !')
                return redirect('register')
            else:
                # Your Account SID twilio
                account_sid = "AC49e8bec60a3167343774d727aad5de8d"
                # Your Auth Token twilio
                auth_token  = "1f4cc794eb5b3dd3b54603aee566384f"

                client = Client(account_sid, auth_token)
                global otps
                otps = str(random.randint(1000,9999))
                message = client.messages.create(
                    to="+91" + phone_number , 
                    
                    from_="+12517661906",
                    body="Hello there! Your Login OTP is"+otps)
                print("1234")
                
                context = {
                    'phone_number': phone_number,
                    'user_name':user_name,

                }
                return render (request, 'accounts/phone_verification.html',context)

        
        else :  
            print("6666")
            if Account.objects.filter(email = user_name).exists():
                user1= Account.objects.filter(email = user_name)
                user1.delete()
                messages.success(request,'entered phone number is not correct !')
                return redirect('register')
           
            else : 
                messages.success(request,'entered phone number is not correct !')
                return redirect('register')

    else : 
            print("3333336")

            messages.success(request,'Please enter correct phone number !')
            return redirect('register')

def otp_verification(request,Phone_number):
    user_name = request.GET.get('name')
    print(Phone_number)
    print(user_name)

    if request.method=='POST':
        fir = request.POST["first"]
        print(fir)
        otp3 =  request.POST['first']+ request.POST['second']+request.POST['third']+request.POST['fourth']
        print(otp3)
       
       
        if otp3 == otps :
            user = Account.objects.filter(email = user_name)
            use = Account.objects.get(email = user_name)
            email = use.email
            first = use.first_name
            last = use.last_name
           
            referel = last+first+email
            user.update(Phone_number = Phone_number , referel_code = referel )
            print(user)
            print("zzz")
            messages.success(request,"registred successfully")
            return redirect ('login')
        else:
            if Account.objects.filter( email = user_name).exists():
                print("''''''''''''''''''''''''''''")
                user = Account.objects.filter(email = user_name)
                user.delete()
                messages.success(request,"register unsuccessfull")
                return redirect ('register')
            else :
                print("/////////////")
                messages.success(request,"register unsuccessfull")
                return redirect ('register')

    else:
        return render (request, 'accounts/phone_verification.html')

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
        print("77777777")
        print(profile)
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
        print("444443434433")
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
            print(pro)

        
            print("010")
            profile = Profile.objects.filter(user = user)
            
            
            print("3")
           
            
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
        print(passw)
        print("5005")


        if new_pass == confirm_pass :
            if passw:
                print("222")
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
    print(cod)
    if user.referel_code != cod :
        print("R")
        if Account.objects.filter(referel_code = cod).exists():
            usr = Account.objects.filter(referel_code = cod)
            print(usr)
            use = Wallet.objects.get(user = user)
            wall = use.balance + 500
            print(wall)
            
            userr = Wallet.objects.filter(user = user)
            userr.update(balance = wall)
            A  = Account.objects.filter(email = user)
            print(A)
            A.update(referel_activated = True)
            messages.success(request,"Referel Successfull. 500 /-  Added to your Wallet, Happy Shopping !")
            return redirect('profile') 
        else:
        
            print("j")
            messages.error(request,"Referel code is wrong !")
            return redirect('profile') 
    else:
        print("j")
        messages.error(request,"Referel code is wrong !")
        return redirect('profile') 
        