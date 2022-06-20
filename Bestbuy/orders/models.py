from tkinter import CASCADE
from django.db import models
from store.models import Product
from category.models import Category

from accounts.models import Account

# Create your models here.

class Payment(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )
    user = models.ForeignKey(Account,on_delete=models.CASCADE, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class Order(models.Model):
    payment_mode = [ 

        ('COD','COD'),
        ('PAYPAL','PAYPAL'),
        ('RAZOR_PAY','RAZORPAY')
    ]
    STATUS = (

        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned')
    )
    user = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=50)
    town= models.CharField(max_length=50 ,blank=True, null=True)
    house = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zip = models.CharField(max_length=10 ,  blank=True, null=True)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    # coupon_applied = models.BooleanField( default= False )
    # coupon = models.CharField( blank=True , max_length=30)

    ip = models.CharField(max_length=20,blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.first_name

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    
    class Meta:
        ordering = ['-created_at','-updated_at']

class Order_Product(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField() 
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def sub_total(self):
        return self.product_price * self.quantity

    

    def __str__(self):
        return self.product.product_name

    class Meta:
        ordering= ('-created_at','-updated_at')
   
