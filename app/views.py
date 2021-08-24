from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import TemplateView
from app.forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product, Profile
from .forms import ProfileForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def login_user(request):
    if request.method == 'POST':
        # AuthenticationForm_can_also_be_used__
        username = request.POST['username']
        password = request.POST['password']
        # print("++++++++++++++++++++++++", username)
        # print("++++++++++++++++++++++++", password)
        user = authenticate(username = username, password = password)
        print("+????????????????????????????????????///++++++++", user)
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
        print(request.POST)
        if form.is_valid():
            form.save()
            print(form)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            login(request, user)
            # User.objects.create()
            Profile.objects.create(
                user=user,
                mobile = form.cleaned_data['number']
            )
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


class UserProfileView(TemplateView):    
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        status_list = Profile.objects.all()
        context['profile'] = status_list.filter(user=self.request.user).first()
        
        return context

    def post(self, request):
        data = request.POST
        print("gsk",data)
        username = data.get('username')
        email = data.get('email')
        bio = data.get('bio')
        state = data.get('state')
        city = data.get('city')
        birth_date = data.get('birth_date')
        number = data.get('number')
        profile_image=request.FILES.get('profile_image')
        print("==============================", profile_image)
        try:
            profile = Profile.objects.filter(user=self.request.user).update(bio=bio, state=state, city=city, birth_date=birth_date, mobile=number)
            profile1 = Profile.objects.get(user=self.request.user)
            profile1.profile_image = profile_image
            profile1.save()
        except ObjectDoesNotExist:
            print("Does Not Exist!")
        
        return redirect('home')

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
