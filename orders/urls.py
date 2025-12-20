from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    #paypal
    path('checkout/paypal/<int:order_id>/', views.paypal_payment, name="paypal_payment"),
    path('paypal-success/<int:order_id>/', views.paypal_success, name="paypal_success"),
    path('paypal-cancel/<int:order_id>/', views.paypal_cancel, name="paypal_cancel"),
]
