from django.db import models
from store.models import Product
from accounts.models import Account


# Create your models here.

class Wishlist(models.Model):
    wishlist_id = models.CharField(max_length=150,blank=True)
   

    def __str__(self):
        return self.wishlist_id

class WishlistItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.product.product_name
   