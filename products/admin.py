from django.contrib import admin
from .models import Category, Product
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','description']
    list_filter=['name']
    prepopulated_fields={'slug':('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display=['name','description','price','category']
    list_filter=['name','price','category']
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product,ProductAdmin)