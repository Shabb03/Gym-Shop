# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from .forms import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

products = Product.objects.all()

def index(request):
    return render(request, 'index.html', {'products':products})

def product_individual(request, prodid):
    product = Product.objects.get(id=prodid)
    return render(request, 'product_individual.html', {'product':product})

class UserSignupView(CreateView):
    model = APIUser
    form_class = UserSignupForm
    template_name = 'user_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class UserLoginView(LoginView):
    template_name='login.html'

@login_required
def logout_user(request):
    logout(request)
    return redirect("/")

@login_required
def add_to_basket(request, prodid):
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        Basket.objects.create(user_id = user)
        basket = Basket.objects.filter(user_id=user, is_active=True).first()
    product = Product.objects.get(id=prodid)
    sbi = BasketItems.objects.filter(basket_id=basket, product_id = product).first()
    if sbi is None:
        sbi = BasketItems(basket_id=basket, product_id = product)
        sbi.save()
    else:
        sbi.quantity = sbi.quantity+1
        sbi.save()
    return render(request, 'product_individual.html', {'product': product, 'added':True})

@login_required
def show_basket(request):
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        return render(request, 'basket.html', {'empty':True})
    else:
        show_items = BasketItems.objects.filter(basket_id=basket)
        if show_items.exists():
            return render(request, 'basket.html', {'basket':basket, 'show_items':show_items})
        else:
            return render(request, 'basket.html', {'empty':True})