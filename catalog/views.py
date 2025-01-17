from django.shortcuts import render, get_object_or_404
from .models import Product, Contact


def home(request):
    # Получаем последние 5 созданных продуктов
    product_list = Product.objects.all()

    # Выводим их в консоль для отладки
    print(product_list)

    # Передаем последние продукты в контекст шаблона
    return render(request, 'product_list.html', {'product_list': product_list})


def contacts(request):
    # Извлекаем все контактные данные из базы данных
    contacts = Contact.objects.all()

    # Передаем контакты в контекст шаблона
    return render(request, 'contacts.html', {'contacts': contacts})


def products_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products_detail.html', {'product': product})