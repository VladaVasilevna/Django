from django import forms


from .models import Client, Message, Mailing

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('email', 'full_name', 'comment')

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('topic_message', 'text_message')
        labels = {
            'topic_message': 'Тема сообщения',
            'text_message': 'Сообщение',
        }


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('message', 'clients', 'repeat', 'start_datetime', 'end_datetime')
        labels = {
            'message': 'Сообщение',
            'clients': 'Получатели',
            'repeat': 'Периодичность отправки',
            'start_datetime': 'Дата и время первой рассылки',
            'end_datetime': 'Дата и время окончания рассылки',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_datetime'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['end_datetime'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
