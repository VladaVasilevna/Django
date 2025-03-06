from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import (AddProductView, CategoryProductsView, ContactsView, DeleteProductView,
                           ProductDetailView, UnpublishProductView, UpdateProductView, HomeView)

app_name = CatalogConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("products/<int:pk>/", cache_page(60)(ProductDetailView.as_view()), name="products_detail"),
    path("product/add/", AddProductView.as_view(), name="add_product"),
    path("product/<int:pk>/update/", UpdateProductView.as_view(), name="update_product"),
    path("product/<int:pk>/delete/", DeleteProductView.as_view(), name="delete_product"),
    path("product/<int:pk>/unpublish/", UnpublishProductView.as_view(), name="unpublish_product"),
    path("category/<int:category_id>/", CategoryProductsView.as_view(), name="category_products"),
]
