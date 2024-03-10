from http import HTTPStatus


from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def test_catalog_endpoint1(self):
        response = Client().get('/catalog/52/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = Client().get('/catalog/1/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = Client().get('/catalog/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = Client().get('catalog/0111/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        response = Client().get('catalog/abc/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        response = Client().get('catalog/a13/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
