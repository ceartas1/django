# Generated by Django 4.2 on 2024-03-24 12:21

from django.db import migrations, models

import catalog.models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="text",
            field=models.TextField(
                validators=[catalog.models.validator], verbose_name="текст"
            ),
        ),
    ]