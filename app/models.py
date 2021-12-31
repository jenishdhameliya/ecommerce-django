from datetime import datetime
from django.db import models
# from django.contrib.auth.models import User
# from django.conf import settings
# from django.core.files.storage import FileSystemStorage


class Category(models.Model):
    name = models.CharField(max_length=50)
  
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
  
    def __str__(self):
        return self.name



class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=100)
  
    # to save the data
    def register(self):
        self.save()
  
    @staticmethod
    def get_customer_by_email(email):
        print("🚀 ~ file: models.py ~ line 33 ~ email", email)
        try:
            data = Customer.objects.filter(email=email)
            print("🚀 ~ file: models.py ~ line 35 ~ data", data)
            return Customer.objects.get(email=email)
        except:
            return False
  
    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
  
        return False

  
    def __str__(self):
        return self.email
    
    
    
class Products(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(
        max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/products/')
  
    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter(id__in=ids)
  
    @staticmethod
    def get_all_products():
        return Products.objects.all()
  
    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter(category=category_id)
        else:
            return Products.get_all_products()



class Order(models.Model):
    product = models.ForeignKey(Products,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.now)
    status = models.BooleanField(default=False)
  
    def placeOrder(self):
        self.save()
  
    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')

class Team(models.Model):
    name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=500, blank=True)
    photo = models.ImageField(upload_to='uploads/products/')
    instagram  = models.URLField(max_length=500)  
    linkedin = models.URLField(max_length=500)
    github = models.URLField(max_length=500)








# # Create your models here.
# # fs = FileSystemStorage(location='/media')

# SIZE_CHOICES = (
#     ('s','S'),
#     ('m', 'M'),
#     ('l','L'),
#     ('xl','XL'),
#     ('xxl','XXL'),
# )


# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.IntegerField()
#     description = models.TextField()
#     size = models.CharField(max_length=6, choices=SIZE_CHOICES)
#     date = models.DateField(auto_now_add=True)
#     category = models.CharField(max_length=200)
#     image = models.ImageField(upload_to="images")




# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(max_length=500, blank=True)
#     state = models.CharField(max_length=30, blank=True)
#     city = models.CharField(max_length=30, blank=True)  
#     birth_date = models.DateField(null=True, blank=True)
#     mobile = models.IntegerField(null=True, blank=True)
#     profile_image = models.ImageField(upload_to="images/")




#     def __str__(self):
#         return f'{self.user.username}'
    
