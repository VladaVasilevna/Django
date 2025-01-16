import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Добавляет продукты в базу данных после удаления существующих'

    def handle(self, *args, **kwargs):
        # Удаляем все существующие продукты и категории
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Загружаем данные из фикстуры
        fixture_path = os.path.join(settings.BASE_DIR, 'catalog_fixture.json')

        try:
            call_command('loaddata', fixture_path)
            self.stdout.write(self.style.SUCCESS('Данные успешно загружены из фикстуры!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке данных: {e}'))
