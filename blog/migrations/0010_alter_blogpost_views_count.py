# Generated by Django 4.2.2 on 2025-02-26 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0009_blogpost_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpost",
            name="views_count",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
