from django.shortcuts import render, get_object_or_404
from .models import Category, Products

# Create your views here.

def product_list(request, category_slug=None): #Si es none mostramos todos los productos

    category = None #Inicialmente será None, si es el caso, se modificará en el if
    categories = Category.objects.all()
    products = Products.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'tienda/product/list.html', {'category':category,
                                                        'categories':categories,
                                                        'products':products})



def product_detail(request, id, slug):
    product = get_object_or_404(Products, id=id, slug=slug, available=True)

    return render(request, 'tienda/product/detail.html', {'product':product})