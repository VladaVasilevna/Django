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
            'end_datetime': 'Дата окончания рассылки',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_datetime'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['end_datetime'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['end_datetime'].required = False

    def clean(self):
        cleaned_data = super().clean()
        repeat = cleaned_data.get('repeat')
        start = cleaned_data.get('start_datetime')
        end = cleaned_data.get('end_datetime')

        if repeat != 'once':
            if not end:
                self.add_error('end_datetime', 'Укажите дату окончания для периодических рассылок')
            elif end < start.date():
                self.add_error('end_datetime', 'Дата окончания не может быть раньше даты первой отправки')
