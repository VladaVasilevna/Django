from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200)  # Заголовок
    content = models.TextField()  # Содержимое
    preview_image = models.ImageField(upload_to='blog_previews/', blank=True, null=True)  # Превью (изображение)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    is_published = models.BooleanField(default=False)  # Признак публикации
    views_count = models.PositiveIntegerField(default=0)  # Количество просмотров

    def __str__(self):
        return self.title
