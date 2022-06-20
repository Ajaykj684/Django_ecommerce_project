from django.db import models
from category.models import Category
from store.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Category_Offer(models.Model):
    category = models.OneToOneField(Category,on_delete=models.CASCADE)
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    active = models.BooleanField( default=True)
    def __str__(self):
            return self.category.category_name

class Todo(models.Model):
    todo_list =models.CharField(max_length=100,blank=True,null= True)

   
