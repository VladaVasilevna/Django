from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from mailing.models import Attempt, Mailing


class Command(BaseCommand):
    def handle(self, *args, **options):
        for mailing in Mailing.objects.filter(status="Создана"):
            if mailing.repeat == "once":
                if mailing.start_datetime <= timezone.now():
                    self.send_mailing(mailing)
            else:
                if mailing.end_datetime and mailing.end_datetime >= timezone.now():
                    self.send_mailing(mailing)
                elif mailing.end_datetime and mailing.end_datetime < timezone.now():
                    mailing.status = "Завершена"
                    mailing.save()

    def send_mailing(self, mailing):
        mailing.status = "Запущена"
        mailing.save()

        # Логика отправки
        for client in mailing.clients.all():
            try:
                send_mail(
                    subject=mailing.message.topic_message,
                    message=mailing.message.text_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                )
                Attempt.objects.create(mailing=mailing, client=client, status="Успешно", server_response="Успешно")
            except Exception as e:
                Attempt.objects.create(mailing=mailing, client=client, status="Не успешно", server_response=str(e))

        # Автоматическое завершение
        if mailing.repeat == "once":
            mailing.status = "Завершена"
            mailing.save()
