from django.db import models

# Create your models here.

#category model
class Category(models.Model):
    name=models.CharField(max_length=50, unique=True)
    description=models.TextField(blank=True)
    slug=models.SlugField(max_length=50,unique=True, blank=True)

    def __str__(self):
        return self.name

#product model
class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=6, decimal_places=2)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    stock=models.PositiveIntegerField(default=0)
    available=models.BooleanField(default=True)
    image=models.ImageField(upload_to='products/', blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name