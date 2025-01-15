from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория продукта", help_text="Введите название категории")
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание", help_text="Введите описание категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Продукт", help_text="Введите название продукта")
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание", help_text="Введите описание продукта"
    )
    image = models.ImageField(
        upload_to="catalog/images/",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение продукта",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите категорию продукта",
        null=True,
        blank=True,
        related_name="products",
    )
    price = models.IntegerField(verbose_name="Цена за покупку", help_text="Введите цену продукта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "category", "price"]

    def __str__(self):
        return self.name

class Contact(models.Model):
    country = models.CharField(max_length=100)
    inn = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return self.country