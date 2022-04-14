from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category
# Create your views here.
from random import randint

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

        return context