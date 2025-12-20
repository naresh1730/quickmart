from django.db import models
from django.utils.text import slugify
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
    slug = models.SlugField(max_length=100, blank=True, null=False, unique=True)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=6, decimal_places=2)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    stock=models.PositiveIntegerField(default=0)
    available=models.BooleanField(default=True)
    image=models.ImageField(upload_to='products/', blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    from django.utils.text import slugify

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
