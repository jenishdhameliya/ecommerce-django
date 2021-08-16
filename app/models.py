from django.db import models
from django.contrib.auth.models import User

# Create your models here.
SIZE_CHOICES = (
    ('s','S'),
    ('m', 'M'),
    ('l','L'),
    ('xl','XL'),
    ('xxl','XXL'),
)


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    size = models.CharField(max_length=6, choices=SIZE_CHOICES)
    date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images", height_field=None, width_field=None, max_length=100)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    state = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    Mobile = models.IntegerField(null=True, blank=True)
    Profile_image = models.ImageField(upload_to="images", height_field=None, width_field=None, max_length=100)

    def __str__(self):
        return f'{self.user.username}'
    
