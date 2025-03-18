from django.core.management.base import BaseCommand
from django.utils import timezone
from mailing.models import Mailing, Client, Attempt
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Отправка рассылок'

    def handle(self, *args, **options):
        for mailing in Mailing.objects.filter(status='Создана'):
            if mailing.repeat == 'once' and mailing.start_datetime <= timezone.now():
                self.send_mailing(mailing)
            elif mailing.end_datetime and mailing.end_datetime >= timezone.now():
                self.send_mailing(mailing)

    def send_mailing(self, mailing):
        mailing.status = 'Запущена'
        mailing.save()

        for client in mailing.clients.all():
            try:
                send_mail(
                    subject=mailing.message.topic_message,
                    message=mailing.message.text_message,
                    from_email='your_email@example.com',
                    recipient_list=[client.email],
                )
                Attempt.objects.create(
                    mailing=mailing,
                    client=client,
                    status='success',
                    server_response='Успешно'
                )
            except Exception as e:
                Attempt.objects.create(
                    mailing=mailing,
                    client=client,
                    status='failed',
                    server_response=str(e)
                )
