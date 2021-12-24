from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.hashers import check_password
from .models import Order
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .models import Customer
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Products
from .models import Category
from django.views import View
import json
import urllib
from django.conf import settings

# Create your views here.
class Index(View):

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('homepage')

    def get(self, request):
        # print()
        # return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')
        return render(request, 'index.html')


def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products()

    data = {}
    data['products'] = products
    data['categories'] = categories

    print('you are : ', request.session.get('email'))
    return render(request, 'product.html', data)


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        print(customer, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                request.session['email'] = customer.email
                request.session['username'] = customer.first_name

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        print(email, password)
        return render(request, 'login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('login')


class Signup (View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        print("655555555555556555555555565555555555555")

        postData = request.POST
        print('postdata', postData)
        first_name = postData.get('fname')
        last_name = postData.get('lname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        recaptcha_response = request.POST.get('g-recaptcha-response')
        print("🚀 ~ file: views.py ~ line 126 ~ recaptcha_response", recaptcha_response)
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        print("🚀 ~ file: views.py ~ line 135 ~ result", result)
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validateCustomer(customer)
        print('----------------->>>>>>>>>>', error_message)

        if not error_message:
            print(first_name, last_name, phone, email, password)
            # customer.is_valid()
            # customer.save()
            customer.password = make_password(customer.password)
            customer.save()
            request.session['customer'] = customer.id
            request.session['email'] = customer.email
            request.session['username'] = customer.first_name
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'register.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "Please Enter your First Name !!"
        elif len(customer.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not customer.last_name:
            error_message = 'Please Enter your Last Name'
        elif len(customer.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif not customer.phone:
            error_message = 'Enter your Phone Number'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message


class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}

        return redirect('cart')


# from app.middlewares.auth import auth_middleware


class OrderView(View):

    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request, 'orders.html', {'orders': orders})


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Products.get_products_by_id(ids)
        print(products)
        return render(request, 'my_cart.html', {'products': products})


def About(request):
    return render(request, 'about.html', {'user': request.user})


def Blog(request):
    return render(request, 'blog.html', {'user': request.user})


def product_detail(request, id):
    single_product = Products.objects.get(id=id)
    return render(request, "product_page.html", {"product": single_product})

 


class UserProfileView(TemplateView):
    template_name = 'profile.html'
    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        print("==============================", context)
        status_list = Customer.objects.all()
        context['profile'] = status_list.filter(user=self.request.user).first()

        return context

    def post(self, request):
        data = request.POST
        print("gsk", data)
        first_name = data.get('fname')
        last_name = data.get('lname')
        phone = data.get('phone')
        email = data.get('email')
        password = data.get('password')
        try:
            profile = Customer.objects.filter(user=self.request.user).update(
                first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)
            profile1 = Customer.objects.get(user=self.request.user)
            profile1.save()
        except ObjectDoesNotExist:
            print("Does Not Exist!")

        return redirect('home')
