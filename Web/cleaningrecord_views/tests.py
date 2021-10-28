from django.http import response
from django.test import TestCase, SimpleTestCase

# Create your tests here.
class SimpleTests(SimpleTestCase):

    def test_home_page_status_code(self):
        response = self.client.get('/home/')
        self.assertAlmostEqual(response.status_code, 200)

    def test_about_page_status_code(self):
        response = self.client.get('/about/')
        self.assertAlmostEqual(response.status_code, 200)

    def test_login_page_status_code(self):
        response = self.client.get('/')
        self.assertAlmostEqual(response.status_code, 200)