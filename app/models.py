from django.db import models

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
