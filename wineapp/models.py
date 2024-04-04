from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Msg(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    mobile=models.BigIntegerField()



class Product(models.Model):
    CAT=((1,'Whiskey'),(2,'Rum'),(3,'vodka'),(4,'Wine'))
    name=models.CharField(max_length=40,verbose_name="product name")
    price=models.FloatField()
    pdetail=models.CharField(max_length=40,verbose_name="product details")
    cat=models.IntegerField(verbose_name="category",choices=CAT)
    is_active=models.BooleanField(default=True,verbose_name="available")
    pimage=models.ImageField(upload_to='image')
    

    def __str__(self):
       return self.name
    

class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)



class Order(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)
