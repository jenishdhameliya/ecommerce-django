from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.About, name='about'),
    path('blog/', views.Blog, name='blog'),
    path('cart/', CartView.as_view(), name='cart'),
    path('productdetail/<id>', views.product_detail, name='productdetail'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('product/', ProductView.as_view(), name='product'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('register/', views.register ,name='register'),
    path('login/', views.login_user ,name='login'),
    path('logout/', views.logout_view ,name='logout'),

]