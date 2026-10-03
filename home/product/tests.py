from django.test import TestCase
from decimal import Decimal
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            description="Electronic gadgets and devices",
        )

    def test_category_str_and_slug(self):
        self.assertEqual(str(self.category), "Electronics")
        self.assertEqual(self.category.slug, "electronics")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Accessories")
        self.product = Product.objects.create(
            category=self.category,
            name="Mechanical Keyboard",
            description="RGB mechanical gaming keyboard",
            price=Decimal("89.99"),
            stock=15,
            is_available=True,
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "Mechanical Keyboard")

    def test_product_fields_and_category(self):
        self.assertEqual(self.product.price, Decimal("89.99"))
        self.assertEqual(self.product.stock, 15)
        self.assertTrue(self.product.is_available)
        self.assertEqual(self.product.category.name, "Accessories")


class SerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Audio")

    def test_category_serializer(self):
        serializer = CategorySerializer(self.category)
        self.assertEqual(serializer.data["name"], "Audio")
        self.assertEqual(serializer.data["slug"], "audio")

    def test_product_serializer_valid(self):
        data = {
            "category": self.category.id,
            "name": "Noise Cancelling Headphones",
            "description": "Premium wireless headphones",
            "price": "199.99",
            "stock": 10,
            "is_available": True,
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()
        self.assertEqual(product.name, "Noise Cancelling Headphones")
        self.assertEqual(serializer.data["category_name"], "Audio")

    def test_invalid_price(self):
        data = {
            "name": "Invalid Product",
            "price": "0.00",
            "stock": 5,
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("price", serializer.errors)
