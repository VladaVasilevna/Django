from django.core.management.base import BaseCommand
from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'Добавляет продукты в базу данных после удаления существующих'

    def handle(self, *args, **kwargs):
        # Удаляем все существующие продукты и категории
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создаем категории
        categories = {
            'Обувь': 'Наша идеальная обувь сочетает в себе комфорт и стиль.',
            'Верхняя одежда': 'Разнообразная коллекция верхней одежды.',
            'Толстовки': 'Толстовки — идеальный выбор для комфорта.',
            'Брюки': 'Широкий ассортимент моделей брюк.',
            'Головные уборы': 'Модные головные уборы для любого стиля.',
        }

        category_instances = {}
        for name, description in categories.items():
            category, created = Category.objects.get_or_create(name=name, defaults={'description': description})
            category_instances[name] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Категория успешно добавлена: {category.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Категория уже существует: {category.name}'))

        # Создаем тестовые продукты
        products = [
            {
                "name": "Хлопковое худи",
                "description": "Декорировано ярко-оранжевым логотипом спереди и на спинке. Изготовлено из плотного хлопка, что обеспечивает долговечность и комфорт.",
                "image": "catalog/images/худи.png",
                "category": category_instances['Толстовки'],
                "price": 66450,
            },
            {
                "name": "Замшевые кеды",
                "description": "Кеды с кожаным подкладом и гибкой подошвой сшиты из замши. Задник и язычок декорированы контрастными вставками с логотипами марки, которым вторят вставки в виде литеры M по бокам.",
                "image": "catalog/images/кеды.png",
                "category": category_instances['Обувь'],
                "price": 39950,
            },
            {
                "name": "Хлопковые брюки",
                "description": "Утрированно свободные брюки сшили из мягкого хлопкового трикотажа. Плотный материал хорошо пропускает воздух, сохраняя оптимальный микроклимат, и не вытягивается со временем. Модель с широким эластичным поясом украсили вышитым логотипом в тон на накладном кармане сзади.",
                "image": "catalog/images/брюки.png",
                "category": category_instances['Брюки'],
                "price": 98050,
            },
            {
                "name": "Хлопковое худи",
                "description": "Для пошива модели силуэта oversize использовали мягкий хлопковый футер с фактурной изнанкой. Материал хорошо пропускает воздух и сохраняет тепло при незначительном снижении температуры.",
                "image": "catalog/images/худи2.png",
                "category": category_instances['Толстовки'],
                "price": 188500,
            },
            {
                "name": "Джинсы",
                "description": "Свободный крой и заниженная линия шагового шва этих голубых джинсов отсылают к силуэту моделей 1990-х.",
                "image": "catalog/images/брюки2.png",
                "category": category_instances['Брюки'],
                "price": 39050,
            },
            {
                "name": "Плащ",
                "description": "Для пошива бежевого двубортного тренча с отлетной кокеткой использовали прочную ткань из мягкого хлопка и шелковистого полиэстера, которая не промокает под небольшим дождем и почти не мнется.",
                "image": "catalog/images/плащ.png",
                "category": category_instances['Верхняя одежда'],
                "price": 92450,
            },
            {
                "name": "Кожаные ботильоны",
                "description": "Ботильоны с квадратным мысом сшили из глянцевой телячьей кожи. Пару на прямом каблуке средней высоты дополнили широкой накладкой, создающей асимметрию. Модель застегивается молнией сбоку.",
                "image": "catalog/images/ботильоны.png",
                "category": category_instances['Обувь'],
                "price": 170500,
            },
            {
                "name": "Шерстяная шапка",
                "description": 'Для создания белоснежной шапки бини использовали мягкую шерстяную пряжу. Материал поддерживает оптимальную температуру, поэтому в модели будет комфортно и в морозный день, и в оттепель. Аксессуар, связанный в технике английской резинки, легко адаптируется к форме головы.',
                "image": 'catalog/images/шапка.png',
                'category': category_instances['Головные уборы'],
                'price': 84550,
            },
            {
                'name': 'Панама',
                'description': 'Нежный розовый цвет этой панамы словно позаимствовали у клубничного зефира. Для прохладной погоды модель с узкими покатыми полями адаптирует материал: ее выполнили из ворсистого текстиля, хорошо сохраняющего тепло. Высокую тулью декорировали логотипом, вышитым шелковистой нитью в тон.',
                'image': 'catalog/images/панама.png',
                'category': category_instances['Головные уборы'],
                'price': 48100,
            },
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(
                name=product_data["name"],
                defaults={
                    'description': product_data["description"],
                    'image': product_data["image"],
                    'category': product_data["category"],
                    'price': product_data["price"],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Продукт успешно добавлен: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Продукт уже существует: {product.name}'))
