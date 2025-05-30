# Generated by Django 4.2.2 on 2025-02-26 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_alter_blogpost_preview_image_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="blogpost",
            options={
                "ordering": ["title"],
                "permissions": [("can_edit_title", "Can edit title"), ("can_edit_content", "Can edit content")],
                "verbose_name": "Пост",
                "verbose_name_plural": "Посты",
            },
        ),
    ]
