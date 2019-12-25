from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.
class Cart(models.Model):
  user      = models.ForeignKey(User, on_delete=models.CASCADE)
  total     = models.DecimalField(default=0.0, max_digits=100, 
                                  decimal_places=2)
  updated   = models.DateTimeField(auto_now=True)
  timestamp = models.DateTimeField(auto_now_add=True) 
  def __str__(self):
    return self.user.username + ' - ' + self.timestamp.strftime("%d/%y/%m %H:%M")
class CartItem(models.Model):
  product = models.ForeignKey(Product, 
                              related_name='orders',
                              on_delete=models.CASCADE)
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  quantity = models.IntegerField(default=0)

