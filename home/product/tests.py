from django.test import TestCase
from decimal import Decimal
from .models import Product
from .serializers import ProductSerializer


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Mechanical Keyboard",
            description="RGB mechanical gaming keyboard",
            price=Decimal("89.99"),
            stock=15,
            is_available=True,
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "Mechanical Keyboard")

    def test_product_fields(self):
        self.assertEqual(self.product.price, Decimal("89.99"))
        self.assertEqual(self.product.stock, 15)
        self.assertTrue(self.product.is_available)


class ProductSerializerTest(TestCase):
    def test_valid_serializer_data(self):
        data = {
            "name": "Wireless Mouse",
            "description": "Ergonomic wireless mouse",
            "price": "49.50",
            "stock": 20,
            "is_available": True,
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()
        self.assertEqual(product.name, "Wireless Mouse")
        self.assertEqual(product.price, Decimal("49.50"))

    def test_invalid_price(self):
        data = {
            "name": "Invalid Product",
            "price": "0.00",
            "stock": 5,
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("price", serializer.errors)
