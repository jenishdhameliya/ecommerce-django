from django.contrib import admin
from django.urls import path
from .views import About, Index, store
from .views import Signup
from .views import Login, logout
from .views import Cart
from .views import CheckOut
from .views import OrderView
from .middlewares.auth import auth_middleware
from . import views
  
urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store/', store, name='store'),
    path('register/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('cart/', auth_middleware(Cart.as_view()), name='cart'),
    path('check-out/', CheckOut.as_view(), name='checkout'),
    path('orders/', auth_middleware(OrderView.as_view()), name='orders'),
    path('about/', views.About, name='about'),
    path('blog/', views.Blog, name='blog'),
    path('productdetail/', views.product_detail, name='productdetail'),
    path('profile/', views.UserProfileView, name='userprofile'),
    
    
    
]