from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (AddProductView, ContactsView, DeleteProductView, HomeView, ProductDetailView,
                           UpdateProductView, UnpublishProductView)

app_name = CatalogConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="products_detail"),
    path("product/add/", AddProductView.as_view(), name="add_product"),
    path("product/<int:pk>/update/", UpdateProductView.as_view(), name="update_product"),
    path("product/<int:pk>/delete/", DeleteProductView.as_view(), name="delete_product"),
    path("product/<int:pk>/unpublish/", UnpublishProductView.as_view(), name="unpublish_product"),
]
