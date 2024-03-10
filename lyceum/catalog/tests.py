from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def test_catalog_endpoint(self):
        response = Client().get('/catalog')
        self.assertEqual(response.status_code, 200)

    def test_catalogint_endpoint(self):
        response = Client().get('/catalog/<int:pk>')
        self.assertEqual(response.status_code, 200)
