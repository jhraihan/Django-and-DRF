from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Service


class SimpleServiceTest(APITestCase):
    def test_create_and_list_service(self):
        # Test DRF create
        response = self.client.post('/aiven/services/', {'name': 'my-db', 'service_type': 'postgres'})
        self.assertEqual(response.status_code, 201)

        # Test DRF list
        response = self.client.get('/aiven/services/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_standard_view(self):
        response = self.client.get('/aiven/')
        self.assertEqual(response.status_code, 200)
