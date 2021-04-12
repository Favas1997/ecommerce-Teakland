from django.db import models

# Create your models here.
class product_category(models.Model):
    category=models.CharField(max_length=100)
    discount=models.IntegerField(default=0)
class products(models.Model):
    product_name=models.CharField(max_length=100)
    category=models.ForeignKey(product_category,on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2,max_digits=7)
    image1=models.ImageField(upload_to='media/')
    image2=models.ImageField(upload_to='media/')
    image3=models.ImageField(upload_to='media/')
    material=models.CharField(max_length=100)
    Diamensions=models.IntegerField()
    CaringInstructions=models.CharField(max_length=150)
    finish=models.CharField(max_length=150)
    DeliveryCondition=models.CharField(max_length=200)

    @property
    def discountprice(self):
        discount_value=(self.price/100)*self.category.discount
        discount_price=self.price-discount_value
        print(discount_price)
        return discount_price
    @property
    def imageurl(self):
        if self.image1 == '':
            image = ''
        else:
            image = self.image1.url
        return image
    
    @property
    def imageurl1(self):
        if self.image2 =='':
            image =''
        else:
            image = self.image2.url
        return image
    
    @property
    def imageurl2(self):
        if self.image3 =='':
            image =''
        else:
            image = self.image3.url
        return image
