# Generated by Django 4.2.2 on 2025-03-17 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0007_remove_mailing_clients_remove_mailing_message_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Mailing",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("start_datetime", models.DateTimeField(verbose_name="Дата и время первой отправки")),
                ("end_datetime", models.DateTimeField(verbose_name="Дата и время окончания отправки")),
                (
                    "status",
                    models.CharField(
                        choices=[("Создана", "Создана"), ("Запущена", "Запущена"), ("Завершена", "Завершена")],
                        default="Создана",
                        max_length=20,
                        verbose_name="Статус",
                    ),
                ),
                ("clients", models.ManyToManyField(to="mailing.client", verbose_name="Получатели")),
                (
                    "message",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="mailing.message", verbose_name="Сообщение"
                    ),
                ),
            ],
            options={
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
            },
        ),
    ]
