from core.models import AbstractModel
from django.core.exceptions import ValidationError
import django.db
from django.db import models


def validator(value):
    if "превосходно" in value.lower().split():
        return
    if "роскошно" in value.lower().split():
        return
    raise ValidationError("нету слово роскошно или превосходно")


class Tag(AbstractModel):
    slug = django.db.models.SlugField(
        "Слаг",
        max_length=200,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Теги"
        verbose_name = "Тег"


class Category(AbstractModel):
    slug = django.db.models.SlugField(
        "Слаг",
        max_length=200,
        unique=True,
        validators=[
            django.core.validators.RegexValidator(r"^[a-zA-Z0-9_-]+$")
        ],
    )
    weight = django.db.models.IntegerField(
        "Вес",
        default=100,
        null=True,
        blank=True,
        validators=[
            django.core.validators.MinValueValidator(0),
            django.core.validators.MaxValueValidator(32767),
        ],
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Категории"
        verbose_name = "Категория"


class Item(AbstractModel):
    tags = models.ManyToManyField(
        Tag, related_name="items", verbose_name="Теги"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категория"
    )
    text = django.db.models.TextField("текст", validators=[validator])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
