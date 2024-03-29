from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils import timezone



# Create your models here.

FLAG_CHOICES = {
    ('New','New'),
    ('Sale','Sale'),
    ('Feature','Feature'),
}

class Product (models.Model):
    name = models.CharField(max_length = 120)
    flag = models.CharField(max_length=10, choices=FLAG_CHOICES)
    price = models.FloatField()
    image = models.ImageField(upload_to='product')
    sku = models.IntegerField()
    subtitle = models.TextField(max_length=500)
    description = models.TextField(max_length=50000)
    tags = TaggableManager()
    brand = models.ForeignKey('Brand', related_name='product_brand', on_delete=models.SET_NULL, null=True, blank=True)




class ProductImages (models.Model):
    product = models.ForeignKey(Product, related_name='product_image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='productimages')




class Brand (models.Model):
    name = models.CharField(max_length = 100)
    image = models.ImageField(upload_to='brand')




class Review (models.Model):
    user = models.ForeignKey(User, related_name='review_user', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, related_name='review_product', on_delete=models.CASCADE)
    review = models.TextField(max_length=500)
    rate = models.IntegerField(choices=[(i,i) for i in range(1,6)])
    created_at = models.DateTimeField(default=timezone.now)
