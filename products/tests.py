from django.test import TestCase
from .models import Category, Product
from decimal import Decimal
# Create your tests here.

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category=Category.objects.create(
            name="Electronics",
            description="Electronics gadgets"
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name,"Electronics")
        self.assertEqual(self.category.description,"Electronics gadgets")
        self.assertIsInstance(self.category, Category)
    def test_category_str(self):
        self.assertEqual(str(self.category), "Electronics")

class ProductModelTest(TestCase):
    def setUp(self):
        self.category=Category.objects.create(name='Books')
        self.product=Product.objects.create(
            name="Django for beginers",
            description="learn django",
            price=Decimal("29.99"),
            category=self.category,
            stock=50,
            available=True 
        )
    
    def test_product_creation(self):
        self.assertEqual(self.product.name,"Django for beginers")
        self.assertEqual(self.product.description,"learn django")
        self.assertEqual(self.product.price,Decimal("29.99"))
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.stock,50)
        self.assertTrue(self.product.available)
        self.assertIsInstance(self.product, Product)

    def test_product_str(self):
        self.assertEqual(str(self.product), "Django for beginers")
    def test_slug_generation(self):
        self.assertEqual(self.product.slug,'django-for-beginers')

    def test_unique_slug_generation(self):
        #create another product with same name
        another_product=Product.objects.create(
            name="Django for Beginers",
            description="Another copy",
            price=Decimal("39.99"),
            category=self.category,
            stock=30
        )

        self.assertNotEqual(self.product.slug,another_product.slug)
        self.assertTrue(another_product.slug.startswith("django-for-beginers"))


