from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Contact
from .forms import ProductForm
from django.core.paginator import Paginator


def home(request):
    # Получаем все продукты для постраничного вывода
    product_list = Product.objects.all()

    # Настройка пагинации
    paginator = Paginator(product_list, 12)  # Показывать по 12 товаров на странице
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request, 'product_list.html', {'product_list': products, 'is_home': True})


def contacts(request):
    # Извлекаем все контактные данные из базы данных
    contacts = Contact.objects.all()
    return render(request, 'contacts.html', {'contacts': contacts})


def products_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products_detail.html', {'product': product})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})
