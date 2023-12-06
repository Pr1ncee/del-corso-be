from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class ProductTestCase(TestCase):
    def test_product_list(self):
        client = APIClient(enforce_csrf_checks=False)
        response = client.get("/api/v1/product/")

        self.assertEqual(response.json(), [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
