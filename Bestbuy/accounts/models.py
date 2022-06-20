from email.headerregistry import Address
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password = None):
        if not email:
            raise ValueError("user must have an email address")

        if not username:
            raise ValueError("User must have username")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
           
        )
        user.is_active = True
        user.set_password(password)
        user.save(using= self._db)
        return user   
    
    def create_superuser(self, first_name,last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name =last_name,
        )
        user.is_admin =True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name =  models.CharField(max_length=50)
    last_name =  models.CharField(max_length=50)
    username =  models.CharField(max_length=50 , unique = True)
    email = models.EmailField(max_length=100 , unique=True)
    Phone_number = models.CharField(max_length=50,null = True, blank=True)


    #required

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin =  models.BooleanField(default=False)
    is_staff =  models.BooleanField(default=False)
    is_active =  models.BooleanField(default=True)
    is_superadmin =  models.BooleanField(default=False)


    referel_code = models.CharField(max_length=50 , null=True , blank = True)
    referel_activated = models.BooleanField(default=False ,null = True )
   
     
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['username','first_name','last_name']
    
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True


class Profile(models.Model):
    gender = (
        ('MEN', 'MEN'),
        ('FEMALE', 'FEMALE'),
        ('OTHERS', 'OTHERS')
    )
    STATUS = (
        ('HOME', 'HOME'),
        ('OFFICE', 'OFFICE'),
        ('OTHERS', 'OTHERS'),
    )
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile/',max_length=500,default='profile/avatar.png')
    first_name =  models.CharField(max_length=50 )
    last_name =  models.CharField(max_length=50, null = True)
  
    Phone_number = models.CharField(max_length=50) 
    gender = models.CharField(max_length=10, choices=gender, default='Male')
    house = models.CharField(max_length=50, null = True)
    town= models.CharField(max_length=50, null = True)
    locality= models.CharField(max_length=50, null = True)
    state = models.CharField(max_length=50, null = True)
    country = models.CharField(max_length=50, null = True)
    Address_type = models.CharField(max_length=10, choices=STATUS, default='HOME')

    
    zip = models.CharField(max_length=10 ,  blank=True, null=True)

    def __str__(self):
        return self.user.username

class Wallet(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    balance = models.FloatField( max_length=20, null = True, default= 0 )
    is_applied = models.BooleanField(default=False)
