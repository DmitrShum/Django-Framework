import os
import json
import random
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def get_hot_product():
    products_list = Product.objects.all()
    return random.sample(list(products_list), 1)[0]

def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return  same_products


def main(request):
    products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:3]
    content = {
        'title': 'Главная',
        'products': products,
    }
    return render(request, 'mainapp/index.html', content)

def products(request, pk=None, page=1):


    title = 'продукты'
    links_menu = ProductCategory.objects.all()
    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все', 'pk': 0}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        paginator = Paginator(products, 2)

        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:                            # если пользователь ввёл непонятное значение, выведется 1 стр
            products_paginator = paginator.page(1)
        except EmptyPage:                                   # если пользователь ввёл большое значение, выведется последняя стр
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
        }
        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'same_products': same_products,
        'hot_product': hot_product,
    }
    return render(request, 'mainapp/products.html', content)

def product(request, pk):
    content = {
        'title': 'Продукт',
        'product': get_object_or_404(Product, pk=pk),
        'links_menu': ProductCategory.objects.all(),
    }
    return render(request, 'mainapp/product.html', content)


def contact(request):
    locations = []
    with open(os.path.join(settings.BASE_DIR, 'contacts.json'), 'r', encoding='utf-8') as f:
        locations = json.load(f)
    content = {
        'title': 'Контакты',
        'locations': locations,
    }
    return render(request, 'mainapp/contact.html', content)
