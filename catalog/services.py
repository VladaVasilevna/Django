from django.core.cache import cache

from catalog.models import Product
from config.settings import CACHE_ENABLED


def get_product_from_cashe():
    """Получает данные по продуктам из кэша, если кэш пуст, получает данные из БД."""
    if not CACHE_ENABLED:
        return Product.objects.filter(is_published=True)
    key = "product_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.filter(is_published=True)
    cache.set(key, products)
    return products


def get_products_by_category(category_id):
    """Получает список продуктов в указанной категории."""
    if not CACHE_ENABLED:
        return Product.objects.filter(category_id=category_id, is_published=True)
    key = f"products_by_category_{category_id}"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.filter(category_id=category_id, is_published=True)
    cache.set(key, products)
    return products
