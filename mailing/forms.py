from django import forms
from django.forms import CheckboxSelectMultiple

from .models import Client, Message, Mailing

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('email', 'full_name', 'comment')

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('topic_message', 'text_message')


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('clients', 'start_datetime', 'end_datetime')

    def save(self, commit=True):
        # Получаем данные из запроса
        topic_message = self.data.get('topic_message')
        text_message = self.data.get('text_message')

        # Создаем и сохраняем сообщение
        message = Message(topic_message=topic_message, text_message=text_message)
        message.save()  # Сначала сохраняем сообщение

        # Создаем рассылку
        mailing = super().save(commit=False)
        mailing.message = message  # Присваиваем сообщение рассылке

        if commit:
            mailing.save()  # Затем сохраняем рассылку
            self.save_m2m()  # Сохраняем многие-ко-многим отношения

        return mailing

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clients'].widget = forms.SelectMultiple()
        self.fields['start_datetime'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['end_datetime'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})