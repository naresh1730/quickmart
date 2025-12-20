from django.db import models
from django.contrib.auth.models import User 
from products.models import Product
# Create your models here.

class Order(models.Model):
    STATUS_CHOICES=(
        ('Pending','Pending'),
        ('Processing','Processing'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=150)
    email=models.EmailField()
    address=models.TextField()
    city=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES,default='Pending')
    created_at=models.DateTimeField(auto_now_add=True)

    #Paypal payment integrations

    payment_id=models.CharField(max_length=100,blank=True,null=True)
    payment_status=models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
