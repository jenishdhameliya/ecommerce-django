from django.contrib import admin
from .models import Product, Profile
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price','category','size','date']

admin.site.register(Product,ProductAdmin)
admin.site.register(Profile)