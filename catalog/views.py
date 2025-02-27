from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ProductForm, ProductModeratorForm
from .models import Category, Contact, Product
from .services import get_product_from_cashe


class HomeView(ListView):
    model = Product
    paginate_by = 12

    def get_queryset(self):
        return get_product_from_cashe()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_home"] = True
        context["categories"] = Category.objects.all()
        return context


class ContactsView(View):
    def get(self, request):
        contacts = Contact.objects.all()
        return render(request, "catalog/contacts.html", {"contacts": contacts})


class ProductDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class UpdateProductView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if (
            user.has_perm("catalog.can_edit_category")
            and user.has_perm("catalog.can_edit_description")
            and user.has_perm("catalog.can_unpublish_product")
        ):
            return ProductModeratorForm
        raise PermissionDenied


class DeleteProductView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm("catalog.delete_product"):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class UnpublishProductView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.has_perm("catalog.can_unpublish_product"):
            raise PermissionDenied
        product = Product.objects.get(pk=pk)
        product.is_published = False
        product.save()
        return redirect(reverse("catalog:home"))


class CategoryProductsView(ListView):
    template_name = "catalog/category_products.html"
    paginate_by = 12

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return Product.objects.filter(category_id=category_id, is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")
        category = get_object_or_404(Category, pk=category_id)
        context["category"] = category
        context["categories"] = Category.objects.all()
        return context
