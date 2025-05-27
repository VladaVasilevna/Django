from django.contrib import admin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в списке объектов
    list_display = ("id", "title", "created_at", "is_published", "views_count", "owner")

    # Поля, по которым можно фильтровать записи
    list_filter = ("is_published", "created_at", "owner")

    # Поля, которые будут доступны для редактирования на странице списка
    list_editable = ("is_published",)

    # Поля для поиска
    search_fields = ("title", "content")

    # Настройка иерархии по дате создания
    date_hierarchy = "created_at"

    # Настройка полей формы при добавлении/редактировании
    fieldsets = (
        (None, {"fields": ("title", "content", "preview_image", "is_published", "owner")}),
        (
            "Advanced options",
            {
                "classes": ("collapse",),
                "fields": ("views_count",),
            },
        ),
    )

    # Сортировка по дате создания
    ordering = ("-created_at",)
