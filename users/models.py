from django.db import models
from Admin.models import * 
from django.contrib.auth.models import User
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    products=models.ForeignKey(products,on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,default=None)
    address=models.CharField(max_length=100,default=None)
    mobile=models.CharField(max_length=50,default=None)
    city=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pincode=models.IntegerField()

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    products=models.ForeignKey(products,on_delete=models.CASCADE)
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    status=models.CharField(max_length=50)
    count = models.PositiveIntegerField()
    price=models.DecimalField(decimal_places=2,max_digits=10)
    payment_method=models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)
    
class myuser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_number=models.CharField(max_length=14)
    image1=models.ImageField(upload_to='media/',null=True)
    
    @property
    def imageurl5(self):
        if self.image1 == '':
            image = ''
        else:
            image = self.image1.url
        return image
class coupon(models.Model):
    coupon_code=models.CharField(max_length=10,null=True)
    date = models.DateField(auto_now_add=True)
    coupon_percentage= models.PositiveIntegerField()
    active = models.BooleanField(default=True)

class Referal(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    referal_code=models.CharField(max_length=20,null=True)
    date = models.DateField(auto_now_add=True)
    coupon_percentage= models.PositiveIntegerField()
    