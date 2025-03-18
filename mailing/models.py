from django.core.exceptions import ValidationError
from django.db import models


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=200, verbose_name="Ф. И. О.")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    editing = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"

class Message(models.Model):
    topic_message = models.CharField(max_length=200, verbose_name="Тема сообщения")
    text_message = models.TextField(default="",verbose_name="Сообщение")

    def __str__(self):
        return self.topic_message

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Mailing(models.Model):
    REPEAT_CHOICES = [
        ('once', 'Один раз'),
        ('daily', 'Ежедневно'),
        ('weekly', '1 раз в неделю'),
        ('monthly', '1 раз в месяц'),
        ('yearly', '1 раз в год'),
    ]

    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    clients = models.ManyToManyField(Client, verbose_name="Получатели")
    repeat = models.CharField(max_length=20, choices=REPEAT_CHOICES, default='once', verbose_name="Периодичность")
    start_datetime = models.DateTimeField(verbose_name="Дата и время первой отправки")
    end_datetime = models.DateTimeField(verbose_name="Дата окончания рассылки", blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('Создана', 'Создана'), ('Запущена', 'Запущена'), ('Завершена', 'Завершена')],
        default='Создана',
        verbose_name="Статус"
    )

    def clean(self):
        if self.repeat != 'once' and self.end_datetime < self.start_datetime:
            raise ValidationError('Дата окончания не может быть раньше даты первой отправки')


    def __str__(self):
        return f"{self.message.topic_message} ({self.status})"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class Attempt(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Получатель")
    attempt_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус")
    server_response = models.TextField(blank=True, verbose_name="Ответ почтового сервера")

    def __str__(self):
        return f"{self.mailing.message.topic_message} ({self.client.email})"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
