from django.shortcuts import render
from .models import Product, Contact


def home(request):
    # Получаем последние 5 созданных продуктов
    latest_products = Product.objects.order_by('-created_at')[:5]

    # Выводим их в консоль для отладки
    print(latest_products)

    # Передаем последние продукты в контекст шаблона
    return render(request, 'home.html', {'latest_products': latest_products})


def contacts(request):
    # Извлекаем все контактные данные из базы данных
    contacts = Contact.objects.all()

    # Передаем контакты в контекст шаблона
    return render(request, 'contacts.html', {'contacts': contacts})
