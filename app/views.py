from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import TemplateView
from app.forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product



# Create your views here.

def login_user(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        print(user.username)
        if user:
            login(request, user)
            messages.success(request, f' wecome {username} !!')
            return redirect('home')
        else:
            messages.error(request,'account done not exit plz sign in')
    # else:        
    #     form = AuthenticationForm()
    return render(request, 'login.html')






def register(request):

    if request.method == "POST":

        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, "register.html", {'form': form})


def home(request):
    return render(request, 'index.html',{'user': request.user})

def About(request):
    return render(request, 'about.html',{'user': request.user})

def Blog(request):
    return render(request, 'blog.html',{'user': request.user})

# class HomeView(TemplateView):
#     template_name = 'index.html'

class CartView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'my_cart.html')

def product_detail(request, id):
    single_product = Product.objects.get(id=id)
    return render(request, "product_page.html",{"product": single_product})

# class ProductDetailView(TemplateView):
#     template_name = 'product_page.html'
#     def get_context_data(self,*args, **kwargs):
#         context = super(ProductDetailView, self).get_context_data(*args,**kwargs)
#         context['products'] = Product.objects.all()
#         return context

class CheckoutView(TemplateView):
    template_name = 'my_checkout.html'

class PaymentView(TemplateView):
    template_name = 'my_payment.html'

class ProductView(TemplateView):
    template_name = 'product.html'
    # extra_context={'users': YourModel.objects.all()}  #other way to pass context
    def get_context_data(self,*args, **kwargs):
        context = super(ProductView, self).get_context_data(*args,**kwargs)
        context['products'] = Product.objects.all()
        return context

def logout_view(request):
    logout(request)
    return redirect('home')