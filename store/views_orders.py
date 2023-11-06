from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Orders, OrderDetails, Customers, Cart
from django.db import transaction
import locale

def ord_orders(request):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    orders = Orders.objects.all()
    for order in orders:
        order.total_amount = locale.currency(order.total_amount, grouping=True)
    return render(request, 'orders.html', {'orders': orders})

def ord_add_order(request):
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
        cart.products.clear()
        return redirect('/orders')
    except:
        return render(request, 'cart.html', {'error': "Algo pasó con tu carrito. Estamos solucionando el problema"})

def ord_order_detail(request, idOrder):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    order = Orders.objects.get(pk=idOrder)
    order.total_amount = locale.currency(order.total_amount, grouping=True)
    order_details = OrderDetails.objects.filter(order=order)
    return render(request, 'order.html', {'order': order, 'order_details': order_details})

def ord_customer(request, idCustomer):
    customer = Customers.objects.get(pk=idCustomer)
    # Lógica para mostrar los detalles del cliente y sus órdenes
    return render(request, 'customer.html', {'customer': customer})
