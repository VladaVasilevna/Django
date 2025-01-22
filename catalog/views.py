from django.shortcuts import render
from .models import Product, Contact
from .forms import ProductForm

from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy


class HomeView(ListView):
    model = Product
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_home'] = True
        return context


class ContactsView(View):
    def get(self, request):
        contacts = Contact.objects.all()
        return render(request, 'catalog/contacts.html', {'contacts': contacts})


class ProductDetailView(DetailView):
    model = Product


class AddProductView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        return super().form_valid(form)
