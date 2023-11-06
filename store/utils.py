from .models import Customers, Products, Cart, Customers, Orders, OrderDetails
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import transaction
import locale

def createUserProfile(request):
     pass1 = request.POST.get('pass1')
     pass2 = request.POST.get('pass2')
     if pass1 != pass2:
        return False
     else:
        user = User.objects.create_user(
                username=request.POST.get('email'),
                password=pass1,
                email=request.POST.get('email'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name')
        )
        user.save()
        return user
     
def get_Products():
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    productslist = list(Products.objects.values())
    for product in productslist:
        product['price'] = locale.currency(product['price'], grouping=True)
    return productslist

def get_Cart(request):
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
        return {'cart': products, 'totalAmount': totalAmount}
    else:
        return False
    
def delete_CartProduct(request, idProduct):
    user = request.user
    customer = Customers.objects.get(email=user.email)
    cart = Cart.objects.get(userID=customer) 
    product_to_remove = Products.objects.get(pk=idProduct)  
    cart.products.remove(product_to_remove)
    return True
    
def get_orders():
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    orders = Orders.objects.all()
    for order in orders:
        order.total_amount = locale.currency(order.total_amount, grouping=True)
    return orders

def add_order(request):
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
    cart.products.clear()
    return True

def order_details(request, idOrder):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    order = get_object_or_404(Orders, pk=idOrder)
    order.total_amount = locale.currency(order.total_amount, grouping=True)
    order_details = OrderDetails.objects.filter(order=idOrder)
    for order_detail in order_details:
        order_detail.subtotal = locale.currency(order_detail.subtotal, grouping=True)
    return {'order': order, 'order_details': order_details}
     

def addProductCart(request, idProduct):
    user = request.user
    customer = Customers.objects.get(email=user.email)
    cart = Cart.objects.get(userID=customer) 
    product_to_add = Products.objects.get(pk=idProduct)  
    cart.products.add(product_to_add)
    return True
