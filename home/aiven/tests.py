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

    def test_service_detail_and_delete(self):
        service = Service.objects.create(name='redis-cache', service_type='redis')
        response = self.client.get(f'/aiven/services/{service.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'redis-cache')

        delete_response = self.client.delete(f'/aiven/services/{service.id}/')
        self.assertEqual(delete_response.status_code, 204)
        self.assertEqual(Service.objects.filter(id=service.id).count(), 0)

    def test_overview_view(self):
        Service.objects.create(name='analytics-db', service_type='postgres', is_active=True)
        response = self.client.get('/aiven/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aiven/overview.html')
        self.assertContains(response, 'analytics-db')

    def test_service_str(self):
        service = Service(name='kafka-stream', service_type='kafka')
        self.assertEqual(str(service), 'kafka-stream (kafka)')
