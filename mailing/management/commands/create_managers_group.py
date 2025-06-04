from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mailing.models import Client, Message, Mailing

class Command(BaseCommand):
    help = 'Создает группу Менеджеры с нужными правами'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='manager')

        # Добавляем права на модели mailing
        models = [Client, Message, Mailing]
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            for perm in permissions:
                group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Группа "manager" создана или обновлена'))
