from django.test import TestCase, Client

class WebsiteTests(TestCase):
    def setUp(self):
        self.c = Client()

    def test_index(self):
        response = self.c.get('/')
        self.assertEquals(response.status_code, 200)