# Generated by Django 5.1.4 on 2025-02-24 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_alter_blogpost_preview_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpost",
            name="preview_image",
            field=models.ImageField(upload_to="blog/images/"),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="views_count",
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
