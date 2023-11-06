from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Products, Customers, Cart
import locale

def pdt_products(request):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    productslist = list(Products.objects.values())
    for product in productslist:
        product['price'] = locale.currency(product['price'], grouping=True)
    return render(request, 'shop.html', {'products': productslist})

def pdt_product_details(request, productName):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    product = Products.objects.get(name=productName)
    product.price = locale.currency(product.price, grouping=True)
    return render(request, 'details.html', {'product': product})

def pdt_addProductToCart(request, idProduct):
    user = request.user
    customer = Customers.objects.get(email=user.email)
    cart = Cart.objects.get(userID=customer) 
    product_to_add = Products.objects.get(pk=idProduct)  
    cart.products.add(product_to_add)
    return redirect('/shop')
