from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('product_detail/<slug:slug>/', views.product_detail, name='product_detail'),
]