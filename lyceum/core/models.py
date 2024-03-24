import django.db


class AbstractModel(django.db.models.Model):
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
