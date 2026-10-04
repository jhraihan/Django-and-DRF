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


from rest_framework.test import APITestCase
from rest_framework import status


class ProductViewTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Monitors")
        self.product = Product.objects.create(
            category=self.category,
            name="4K Gaming Monitor",
            description="Ultra HD 144Hz monitor",
            price=Decimal("399.99"),
            stock=8,
            is_available=True,
        )

    def test_product_list_and_create(self):
        # Test List (GET)
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Test Create (POST)
        new_data = {
            "category": self.category.id,
            "name": "Desk Mat",
            "price": "29.99",
            "stock": 50,
            "is_available": True,
        }
        create_resp = self.client.post('/products/', new_data)
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_product_detail_and_update_and_delete(self):
        # Retrieve
        resp = self.client.get(f'/products/{self.product.id}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['name'], "4K Gaming Monitor")

        # Update
        update_resp = self.client.put(
            f'/products/{self.product.id}/',
            {"price": "349.99"},
            format='json',
        )
        self.assertEqual(update_resp.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, Decimal("349.99"))

        # Delete
        del_resp = self.client.delete(f'/products/{self.product.id}/')
        self.assertEqual(del_resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.filter(id=self.product.id).count(), 0)

    def test_category_list_and_create(self):
        resp = self.client.get('/products/categories/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

        create_resp = self.client.post('/products/categories/', {'name': 'Laptops'})
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_product_summary(self):
        resp = self.client.get('/products/summary/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['total_products'], 1)
        self.assertEqual(resp.data['available_products'], 1)
        self.assertEqual(resp.data['total_categories'], 1)

    def test_cbv_and_viewset(self):
        # Test Generic CBV
        cbv_resp = self.client.get('/products/cbv/')
        self.assertEqual(cbv_resp.status_code, status.HTTP_200_OK)

        # Test ViewSet route
        vs_resp = self.client.get('/products/api/viewset/')
        self.assertEqual(vs_resp.status_code, status.HTTP_200_OK)

