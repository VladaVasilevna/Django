from django.db import models

from users.models import User


class BlogPost(models.Model):
    title = models.CharField(max_length=200)  # Заголовок
    content = models.TextField()  # Содержимое
    preview_image = models.ImageField(upload_to="blog/images/")  # Превью (изображение)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    is_published = models.BooleanField(default=False)  # Признак публикации
    views_count = models.PositiveIntegerField(default=0, editable=True)  # Количество просмотров
    owner = models.ForeignKey(User, verbose_name="Владелец", help_text="Укажите владельца поста", blank=True, null=True, on_delete=models.SET_NULL) # Владелец публикации

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        permissions = [
            ("can_edit_content", "Can edit content"),
            ("can_edit_is_published", "Can edit is published"),
        ]
