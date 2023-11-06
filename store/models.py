from django.db import models

class Customers(models.Model):
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100) 
    phone_number = models.CharField(max_length=20)
   
    def __str__(self):
        return self.email

class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    inventory = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', default='default_image.jpg')
    category = models.CharField(max_length=50) 
    weight = models.DecimalField(max_digits=6, decimal_places=0)  
    dimensions = models.CharField(max_length=20)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    userID = models.ForeignKey(Customers, on_delete=models.CASCADE, null=True, default=None)
    products = models.ManyToManyField(Products)

class Orders(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    order_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.TextField()  
    total_amount = models.DecimalField(max_digits=10, decimal_places=0)
    order_status = models.CharField(max_length=20)  

class OrderDetails(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, default=None)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=0)
    