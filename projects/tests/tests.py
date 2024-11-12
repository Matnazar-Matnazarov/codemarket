from django.test import TestCase
from ..views.home import ProjectAnalysisView
from django.urls import reverse


# Create your tests here.
# 0288D1
class TestProjectAnalysisView(TestCase):
    def test_project_analysis_view(self):
        url = "http://localhost:9000/projects/project-analysis/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # print(response.data)
