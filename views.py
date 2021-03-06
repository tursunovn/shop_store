from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Product, Category, Review
# Create your views here.
from random import randint
from .forms import LoginForm, RegistrationForm, ReviewForm
from django.contrib.auth import login, logout
from django.contrib import messages

class ProductList(ListView):
    model = Product
    context_object_name = 'categories'
    extra_context = {
        'title': 'Главная страница'
    }
    template_name = 'store/product_list.html'

    def get_queryset(self):
        categories = Category.objects.all()
        data = []

        for category in categories:
            # products = Product.objects.filter(category=category, quantity__gt=0)[:4]
            products = category.products.filter(quantity__gt=0)[:4]

            if category.image:
                image = category.image.url
            else:
                image = 'http://time-logo.ru/images/detailed/2/%D0%9C%D0%BE%D0%B4%D0%B5%D0%BB%D1%8C_77_%D1%81%D0%B5%D1%80%D0%B5%D0%B1%D1%80%D0%B8%D1%81%D1%82%D1%8B%D0%B9_1_x05k-3c.jpg'

            data.append({
                'title': category,
                'image': image,
                'products': products
            })

        return data


class ProductListByCategory(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/category_product_list.html'

    def get_queryset(self):
        sort_field = self.request.GET.get('sort')
        products = Product.objects.filter(
            category__slug=self.kwargs['slug'],
            quantity__gt=0
        )

        if sort_field:
            products = products.order_by(sort_field)

        return products

class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = Product.objects.get(slug=self.kwargs['slug']).title

        products = Product.objects.filter(quantity__gt=0)
        data = []

        for i in range(4):
            random_index = randint(0, len(products)-1)
            product = products[random_index]
            if product not in data:
                data.append(product)

        context['products'] = data
        context['reviews'] = Review.objects.filter(product__slug = self.kwargs['slug'])
        if self.request.user.is_authenticated:
            context['review_form'] = ReviewForm()

        return context

def login_registration(request):
    context = {
        'login_form':LoginForm(),
        'registration_form': RegistrationForm(),
        'title': 'Войти или зарегистрироваться'
    }
    return render(request, 'store/login_registration.html', context)


def user_login(request):
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('product_list')
    else:
        messages.error(request, 'Не верное имя пользователя или пароль')
        return redirect('login_registration')


def user_logout(request):
    logout(request)
    return redirect('product_list')

def register(request):
    form = RegistrationForm(data=request.POST)
    if form.is_valid():
        user = form.save()
        messages.success(request, 'Отлично! Вы зарегитсрировались! Войдите в аакаунт!')
    else:
        messages.error(request, 'Что-то пошло не так')
    return redirect('login_registration')

def save_review(request, product_slug):
    form = ReviewForm(data=request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.author = request.user
        product = Product.objects.get(slug=product_slug)
        review.product = product
        review.save()
    else:
        pass
    return redirect('product_detail', product_slug)