from django.contrib import admin

from .models import Client, Mailing, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "user")  # Показывать поле user в списке
    fields = ("email", "full_name", "comment", "user", "editing")  # Поля для редактирования
    list_filter = ("user",)  # Фильтр по владельцу

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("topic_message", "user")
    fields = ("topic_message", "text_message", "user")
    list_filter = ("user",)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("message", "user", "repeat", "start_datetime", "end_datetime", "status")
    list_filter = ("user", "status", "repeat")
