from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Order, OrderItem
#paypal
from django.conf import settings
import paypalrestsdk
# Create your views here.

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty")
        return redirect('cart:view_cart')

    total = sum(item['price'] * item['quantity'] for item in cart.values())

    # Pre-create a pending order for PayPal button
    # order, created = Order.objects.get_or_create(
    #     user=request.user,
    #     status="Pending",
    #     total_price=total
    # )

    if request.method == "POST":
        # Save shipping info
        order=Order.objects.create(
            user=request.user,
            status="Pending",
            total_price=total,
            full_name = request.POST.get('full_name'),
            email = request.POST.get('email'),
            address = request.POST.get('address'),
            city = request.POST.get('city'),
            phone = request.POST.get('phone'),
        )

        # Create order items
        for slug, item in cart.items():
            product = Product.objects.get(slug=slug)
            OrderItem.objects.get_or_create(
                order=order,
                product=product,
                price=item['price'],
                quantity=item['quantity'],
            )

        
        messages.success(request, "Order created. Proceed to PayPal for payment.")
        return redirect('orders:paypal_payment', order.id)

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'total': total,
    })

@login_required
def my_orders(request):
    orders=Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders':orders})

@login_required
def order_detail(request,order_id):
    order=Order.objects.get(id=order_id, user=request.user)
    return render(request,'orders/order_detail.html',{'order':order})

#Configure Paypal SDK

paypalrestsdk.configure({
    "mode":settings.PAYPAL_MODE,
    "client_id":settings.PAYPAL_CLIENT_ID,
    "client_secret":settings.PAYPAL_CLIENT_SECRET,
})

def paypal_payment(request,order_id):
    order=get_object_or_404(Order,id=order_id, user=request.user)

    #create Payment
    payment=paypalrestsdk.Payment({
        "intent":"sale",
        "payer":{
            "payment_method":"paypal"
        },
        "redirect_urls":{
            "return_url" : request.build_absolute_uri(f"/orders/paypal-success/{order.id}/"),
            "cancel_url" : request.build_absolute_uri(f"/orders/paypal-cancel/{order.id}/"),
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name" : f"Order #{order.id}",
                    "sku" : f"order-{order.id}",
                    "price" : str(order.total_price),
                    "currency" : "USD",
                    "quantity" : 1,
                }]
            },
            "amount" : {
                "total" : str(order.total_price),
                "currency" : "USD",                
            },
            "description" : f"Payment for Order #{order.id}",

        }]
    })
    
    if payment.create():
        order.payment_id=payment.id
        order.save()
        #redirect url to payment approval url
        for link in payment.links:
            if link.rel == 'approval_url':
                return redirect(link.href)
        return render(request, "orders/payment_error.html", {"error": "Approval URL not found"})
    else:
        #payment creation failed
        return render(request, "orders/payment_error.html", {"error":payment.error})

#handle success url
def paypal_success(request, order_id):
    order = get_object_or_404(Order,id=order_id, user=request.user)
    payment_id = order.payment_id
    payer_id = request.GET.get('PayerID')
    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id" : payer_id}):
        order.payment_status="Completed"
        order.status="Processing"
        order.transaction_id = payment.transactions[0].related_resources[0].sale.id
        order.payer_email = payment.payer.payer_info.email
        order.payment_amount = payment.transactions[0].amount.total
        order.payment_currency = payment.transactions[0].amount.currency
        order.payment_time = payment.create_time
        order.save()

        for item in order.items.all():
            product=item.product
            if product.stock >= item.quantity:
                product.stock -= item.quantity
                product.save()
            else:
                order.payment_status="Failed"
                order.save()
                messages.error(request, f" Product {product.name} is out of stock.")
                return redirect('orders:order_detail', order.id)
        if 'cart' in request.session:
            del request.session['cart']
        messages.success(request, "Payment successful! Your order is now processing.")
        return redirect('orders:order_detail', order.id)
    else:
        order.payment_status="Failed"
        order.save()
        return render(request,'orders/payment_error.html', {"error" : payment.error})

#cancel url
def paypal_cancel(request,order_id):
    order=get_object_or_404(Order, id=order_id, user=request.user)
    order.payment_status="Cancelled"
    order.save()
    return redirect('orders:order_detail',order.id)


