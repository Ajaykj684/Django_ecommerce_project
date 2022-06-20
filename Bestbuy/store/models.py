from django.db import models
from category . models import Category
import django_extensions
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Product(models.Model):

    
    product_name = models.CharField(max_length=200, unique=True)
    slug         = AutoSlugField(populate_from=['product_name'] ,unique=True)
    description  = models.TextField(max_length=500, blank=True)
    price        = models.IntegerField()
    offer_price = models.IntegerField(null=True, blank=True)
    offer_perc =  models.IntegerField(null=True, blank=True, default= 0)
    image1       = models.ImageField(upload_to = 'photos/products')
    image2       = models.ImageField(upload_to = 'photos/products',blank=True)
    image3       = models.ImageField(upload_to = 'photos/products',blank=True)
    

    stock        = models.IntegerField()
    Is_available = models.BooleanField(default=True)
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add =True)
    modified_date = models.DateTimeField(auto_now=True)
    product_offer = models.IntegerField(null=True, blank=True ,default= 0, validators=[MinValueValidator(0),MaxValueValidator(100)])
    Is_offer_active = models.BooleanField(default=True)
    
    
    def get_url(self):
        return reverse('product_page',args=[self.category.slug, self.slug])
    
    
    def  __str__(self):
        return self.product_name