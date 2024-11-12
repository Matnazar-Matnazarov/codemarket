from django.test import TestCase
from rest_framework import status


class TestProjectViewSet(TestCase):
    def setUp(self):
        self.url = "http://localhost:9000/projects/project/projects/"

    def test_project_list(self):
        """Project ro'yxatini olish testi"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertIn("data", response.data)
        self.assertIn("timestamp", response.data)
