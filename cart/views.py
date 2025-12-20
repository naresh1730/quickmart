from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.contrib import messages
# Create your views here.

#add products to cart
def add_to_cart(request,slug):
    product=get_object_or_404(Product, slug=slug)
    cart=request.session.get('cart',{})
    if slug in cart:
        cart[slug]['quantity']+=1 
    else:
        cart[slug]={
            'name':product.name,
            'price':float(product.price),
            'quantity':1,
            'image':product.image.url if product.image else None 
        }
    request.session['cart']=cart 
    messages.success(request, f'added {product.name} to cart.')
    return redirect('cart:view_cart')
#remove product from cart

def remove_from_cart(request,slug):
    cart=request.session.get('cart',{})
    if slug in cart:
        del cart[slug]
        request.session['cart']=cart 
        messages.success(request, "Product removed from cart")
    return redirect('cart:view_cart')

#update quantity
def update_cart(request,slug):
    if request.method=="POST":
        quantity=int(request.POST.get('quantity',1))
        cart=request.session.get('cart',{})
        if slug in cart:
            cart[slug]['quantity']=quantity 
            request.session['cart']=cart
            messages.success(request,'Cart updated successfully')
    return redirect('cart:view_cart')

#view cart

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for slug, item in cart.items():
        subtotal = item['price'] * item['quantity']
        item['subtotal'] = subtotal
        item['slug'] = slug  # for URLs in template
        cart_items.append(item)
        total += subtotal

    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'cart/cart.html', context)
