from django.core.exceptions import ValidationError
import django.db
from django.db import models


def validator(value):
    if "превосходно" in value.lower().split():
        return
    if "роскошно" in value.lower().split():
        return
    raise ValidationError("нету слово роскошно или превосходно")


class Core(django.db.models.Model):
    name = django.db.models.CharField(
        "название",
        max_length=150,
    )

    is_published = django.db.models.BooleanField(
        "опубликовано",
        default=True,
    )

    class Meta:
        abstract = True


class Tag(Core):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Теги"
        verbose_name = "Тег"


class Category(Core):
    slug = django.db.models.SlugField(
        "Слаг",
        max_length=200,
        unique=True,
    )
    weight = django.db.models.IntegerField(
        "Вес", default=100, null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Категории"
        verbose_name = "Категория"


class Item(Core):
    tags = models.ManyToManyField(
        Tag, related_name="items", verbose_name="теги"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="категория"
    )
    text = django.db.models.TextField("текст", validators=[validator])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
