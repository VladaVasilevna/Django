from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Client, Message, Mailing, Attempt
from .forms import ClientForm, MessageForm, MailingForm
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = '/clients/'

class ClientListView(ListView):
    model = Client
    queryset = Client.objects.all()

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = '/clients/'

class ClientDeleteView(DeleteView):
    model = Client
    success_url = '/clients/'

class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = '/messages/'

class MessageListView(ListView):
    model = Message
    queryset = Message.objects.all()

class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = '/messages/'

class MessageDeleteView(DeleteView):
    model = Message
    success_url = '/messages/'

class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = '/mailings/'

class MailingListView(ListView):
    model = Mailing
    queryset = Mailing.objects.all()

class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = '/mailings/'

class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = '/mailings/'

def index(request):
    mailings_count = Mailing.objects.count()
    active_mailings_count = Mailing.objects.filter(status='started').count()
    unique_clients_count = Client.objects.count()

    context = {
        'mailings_count': mailings_count,
        'active_mailings_count': active_mailings_count,
        'unique_clients_count': unique_clients_count,
    }

    return render(request, 'mailing/index.html', context)

def send_mailing(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    for client in mailing.clients.all():
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email],
            )
            Attempt.objects.create(mailing=mailing, status='success')
        except Exception as e:
            Attempt.objects.create(mailing=mailing, status='failed', response=str(e))
    return redirect('/mailings/')
