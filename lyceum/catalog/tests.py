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
    @classmethod
    def setUpClass(cls):
        cls.category = catalog.models.Category(
            name="test",
            slug="test",
        )
        cls.category.full_clean()
        cls.category.save()
        cls.tag = catalog.models.Tag(
            name="test",
            slug="test",
        )
        cls.tag.full_clean()
        cls.tag.save()
        return super().setUpClass()

    def test_add_validate_item(self):
        item = catalog.models.Item(
            name="test",
            text="превосходно",
            category=self.category,
        )
        item.full_clean()
        item.save()
        item.tags.add(self.tag)
        item.full_clean()
        item.save()

    def test_add_novalidate_item(self):
        with self.assertRaises(ValidationError):
            item = catalog.models.Item(
                name="test",
                text="test",
                category=self.category,
            )
            item.full_clean()
            item.save()
            item.tags.add(self.tag)
            item.full_clean()
            item.save()

    def test_add_validate_category(self):
        category = catalog.models.Category(
            name="test",
            slug="test1",
            weight="100"
        )
        category.full_clean()
        category.save()

    def test_add_validate_tag(self):
        tag = catalog.models.Tag(
            name="test",
            slug="test1",
        )
        tag.full_clean()
        tag.save()
