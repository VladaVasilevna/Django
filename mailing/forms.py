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

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('clients', 'start_datetime', 'end_datetime')

    def save(self, commit=True):
        message = Message(topic_message=self.cleaned_data['topic_message'], text_message=self.cleaned_data['text_message'])
        if commit:
            message.save()
        mailing = super().save(commit=False)
        mailing.message = message
        if commit:
            mailing.save()
        return mailing

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_datetime'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['end_datetime'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
