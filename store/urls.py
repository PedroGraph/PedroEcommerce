from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('shop', views.products, name='shop'),
    path('cart', views.cart, name='cart'),
    path('cart/<int:idProduct>/delete', views.deleteCartProduct, name='deleteCartProduct'),
    path('login', views.login_view, name='login'), 
    path('login/user/', views.loginCredentials, name='loginCredentials'), 
    path('signup', views.signup, name='signup'),
    path('signup/user/', views.signupCredentials, name='signupCredentials'),
    path('logout', views.logoutCredentials, name='logout'),
    path('orders', views.orders, name='orders'),
    path('order/<int:idOrder>', views.order_detail, name='orderDetails'),
    path('order/add', views.addOrder, name='order'),
    # path('customer/<int:idCustomer>', views.customer, name='customer'),
    path('product/<str:productName>', views.product_details, name='productdetails'),
    path('product/<int:idProduct>/add', views.addProductToCart, name='addProductToCart'),
]    
