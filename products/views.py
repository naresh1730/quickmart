from django.shortcuts import render, get_object_or_404
from .models import Category, Product
# Create your views here.

def category_list(request):
    categories=Category.objects.all()
    return render(request, 'products/category_list.html', {'categories':categories})

def product_detail(request,slug):
    category=get_object_or_404(Category, slug=slug)
    products=Product.objects.filter(category=category)
    return render(request,'products/product_detail.html', {'products':products})
