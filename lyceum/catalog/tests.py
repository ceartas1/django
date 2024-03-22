from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.test import Client, TestCase
import parameterized

import catalog.models


class HomePageEndPointTest(TestCase):
    def test_catalog_main_endpoint(self):
        respone = Client().get("/catalog/")
        status_code = respone.status_code
        self.assertEqual(status_code, HTTPStatus.OK)

    @parameterized.parameterized.expand(
        [
            ("0", HTTPStatus.OK),
            ("1", HTTPStatus.OK),
            ("100", HTTPStatus.OK),
            ("110", HTTPStatus.OK),
            ("abs", HTTPStatus.NOT_FOUND),
            ("1a", HTTPStatus.NOT_FOUND),
            ("a1", HTTPStatus.NOT_FOUND),
            ("%1", HTTPStatus.NOT_FOUND),
            ("1%", HTTPStatus.NOT_FOUND),
            ("0.121", HTTPStatus.NOT_FOUND),
            ("9.012", HTTPStatus.NOT_FOUND),
        ]
    )
    def test_catalog_item_detail_endpoint(self, param, expected_status):
        with self.subTest(param=f"/catalog/{param}/"):
            respone = Client().get(f"/catalog/{param}/")
            status_code = respone.status_code
            self.assertEqual(status_code, expected_status)


class CatalogDBTest(TestCase):
    def test_add_validate_item(self):
        item = catalog.models.Item(
            name="test",
            text="превосходно",
        )
        item.full_clean()
        item.save()

    def test_add_novalidate_item(self):
        with self.assertRaises(ValidationError):
            item = catalog.models.Item(
                name="test",
                text="test",
            )
            item.full_clean()
            item.save()
