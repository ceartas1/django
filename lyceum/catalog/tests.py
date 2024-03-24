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

    def test_add_validate_item(self):  # тест на валидатор без ошибок
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

    def test_add_novalidate_item(self):  # тест на ошибку валидтора
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

    def test_delete_item(self):  # удаление элемента
        item = catalog.models.Item(
            name="test",
            text="превосходно",
            category=self.category,
        )
        item.full_clean()
        item.save()
        item.delete()
        print("удалено")

    def test_search_items_by_category(
        self,
    ):  # Создание категорий с разными slag
        category1 = catalog.models.Category.objects.create(
            name="Category 1", slug="роскошно"
        )
        category2 = catalog.models.Category.objects.create(
            name="Category 2", slug="превосходно"
        )

        item1 = catalog.models.Item(
            name="item1",
            text="роскошно",
            category=category1,
        )
        item1.full_clean()
        item1.save()

        item2 = catalog.models.Item(
            name="item2",
            text="превосходно",
            category=category2,
        )
        item2.full_clean()
        item2.save()

        items_in_category1 = catalog.models.Item.objects.filter(
            category=category1
        )
        items_in_category2 = catalog.models.Item.objects.filter(
            category=category2
        )

        self.assertEqual(items_in_category1.count(), 1)
        self.assertEqual(items_in_category2.count(), 1)
