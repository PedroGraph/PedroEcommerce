
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Customers, Products, Cart, Customers, Orders, OrderDetails
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
import locale

def login_view(request): 
    return render(request, 'login.html')

def loginCredentials(request):
    if request.method == 'POST':
        try:
            user = authenticate(request, username=request.POST.get('email'), password=request.POST.get('pass'))
            if user is not None:
                login(request, user)
                return redirect('/shop')  
            else:
                return render(request, 'login.html', {'error': "Credenciales incorrectas"})
        except:
            return render(request, 'login.html', {'error': "Error de autenticación"})  
    else:
        return render(request, 'login.html') 
        
@login_required
def logoutCredentials (request):
    logout(request)
    return redirect('/shop')

def signup(request):
    return render(request, 'signup.html')

def signupCredentials(request):
    if request.method == 'POST':
       try:
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1 != pass2:
            return render(request, 'signup.html', {'error': "Las contraseñas no coinciden"})
        else:
            user = User.objects.create_user(
                username=request.POST.get('email'),
                password=pass1,
                email=request.POST.get('email'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name')
            )
            user.save()
            login(request, user)
            return redirect('/shop')
       except:
            return render(request, 'signup.html', {'error': "El usuario ya existe"})

def home(request):
    return render(request, 'index.html')

def products(request):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    productslist = list(Products.objects.values())
    for product in productslist:
        product['price'] = locale.currency(product['price'], grouping=True)
    return render(request, 'shop.html', {'products': productslist})

@login_required
def cart(request):
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        user = request.user
        customer = Customers.objects.get(email=user.email)
        totalAmount = 0
        cart = get_object_or_404(Cart, userID=customer)
        products = []
        if cart :
            for product in cart.products.all():
                totalAmount += product.price
                product.price = locale.currency(product.price, grouping=True)
                products.append(product)

            totalAmount = locale.currency(totalAmount, grouping=True)
            return render(request, 'cart.html', {'cart': products, 'totalAmount': totalAmount})
        else:
            return render(request, 'cart.html', {'error': "No hay productos en el carrito"})
    except:
        return render(request, 'cart.html', {'error': "No hay productos en el carrito"})
    

@login_required
def orders(request):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    orders = Orders.objects.all()
    for order in orders:
        order.total_amount = locale.currency(order.total_amount, grouping=True)
    return render(request, 'orders.html', {'orders': orders})

@login_required
def addOrder(request):
    try:
        user = request.user
        customer = Customers.objects.get(email=user.email)
        cart = Cart.objects.get(userID=customer)

        # Obtén los productos, cantidades y subtotales del carrito
        cart_items = []
        total_amount = 0

        customer.phone_number =  request.POST.get('phone_number')
        customer.save()

        for product in cart.products.all():
            quantity = request.POST.get(f'quantity_{product.id}') 
            quantity = int(quantity) if quantity else 0

            subtotal = product.price * quantity

            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })

            total_amount += subtotal

        # Crea una nueva instancia de Orders y guárdala en la base de datos
        with transaction.atomic():
            order = Orders.objects.create(
                customer=customer,
                payment_method=request.POST.get('payment_method'),
                shipping_address=request.POST.get('shipping_address'),
                total_amount=total_amount,
                order_status="Pendiente"  # Puedes ajustar el estado del pedido
            )

            # Crea instancias de OrderDetails para cada producto en el carrito
            for item in cart_items:
                product = item['product']
                quantity = item['quantity']
                subtotal = item['subtotal']
                OrderDetails.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    subtotal=subtotal
                )

        # Limpia el carrito (elimina todos los productos)
        # cart.products.clear()
        return redirect('/orders')
    except:
        return render(request, 'cart.html', {'error': "Algo pasó con tu carrito. Estamos solucionando el problema"})
    
@login_required
def order_detail(request, idOrder):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    order = get_object_or_404(Orders, pk=idOrder)
    order.total_amount = locale.currency(order.total_amount, grouping=True)
    order_details = OrderDetails.objects.filter(order=idOrder)
    for order_detail in order_details:
        order_detail.subtotal = locale.currency(order_detail.subtotal, grouping=True)
    return render(request, 'order.html', {'order': order, 'order_details': order_details})



@login_required
def customer(request, idCustomer):
    customer =   get_object_or_404(Customers, id=idCustomer) 
    return HttpResponse(" cliente : %s" % customer.name)

@login_required
def productdetails(request, product):
    return HttpResponse("productdetails")

def deleteCartProduct(request, idProduct):
    user = request.user
    customer = Customers.objects.get(email=user.email)
    cart = Cart.objects.get(userID=customer) 
    product_to_remove = Products.objects.get(pk=idProduct)  
    cart.products.remove(product_to_remove)
    return redirect('/cart')

@login_required
def addProductToCart(request, idProduct):
    user = request.user
    customer = Customers.objects.get(email=user.email)
    cart = Cart.objects.get(userID=customer) 
    product_to_add = Products.objects.get(pk=idProduct)  
    cart.products.add(product_to_add)
    return redirect('/shop')

@login_required
def product_details(request, productName):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    product = Products.objects.get(name=productName)
    product.price = locale.currency(product.price, grouping=True)
    return render(request, 'details.html', {'product': product})
