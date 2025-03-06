from django.db import models
from django.utils import timezone

class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=200, verbose_name="Ф. И. О.")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    editing = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class Message(models.Model):
    topic_message = models.CharField(max_length=200, verbose_name="Тема сообщения")
    text_message = models.TextField(default="",verbose_name="Сообщение")

    def __str__(self):
        return self.topic_message

class Mailing(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    clients = models.ManyToManyField(Client, verbose_name="Получатели")
    start_datetime = models.DateTimeField(verbose_name="Дата и время первой отправки")
    end_datetime = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(max_length=20, default="Создана", verbose_name="Статус")

    def __str__(self):
        return f"{self.message.topic_message} ({self.status})"

class Attempt(models.Model):
    attempt_time = models.DateTimeField(default=timezone.now, verbose_name="Дата и время попытки")
    status = models.CharField(max_length=10, choices=[('success', 'Успешно'), ('failed', 'Не успешно')], verbose_name="Статус")
    response = models.TextField(blank=True, null=True, verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")

    def __str__(self):
        return f"{self.mailing.message.subject} ({self.status})"
