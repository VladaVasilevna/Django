from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Client, Message, Mailing, Attempt
from .forms import ClientForm, MessageForm, MailingForm
from django.core.mail import send_mail
from django.conf import settings

class ClientCreateView(View):
    def get(self, request):
        form = ClientForm()
        clients = Client.objects.all().order_by('id')
        editing_client = request.session.get('editing_client', None)
        return render(request, 'mailing/client_form.html', {'form': form, 'clients': clients, 'editing_client': editing_client})

    def post(self, request):
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.path)
        editing_client = request.session.get('editing_client', None)
        return render(request, 'mailing/client_form.html', {'form': form, 'clients': Client.objects.all().order_by('id'), 'editing_client': editing_client})

class ClientEditView(View):
    def get(self, request, pk):
        request.session['editing_client'] = pk
        return redirect('/mailing/clients/create/')

class ClientSaveView(View):
    def post(self, request, pk):
        client = Client.objects.get(pk=pk)
        client.full_name = request.POST.get('full_name', client.full_name)
        client.email = request.POST.get('email', client.email)
        client.comment = request.POST.get('comment', client.comment)
        client.save()
        request.session['editing_client'] = None
        return redirect('/mailing/clients/create/')

class ClientCancelView(View):
    def get(self, request, pk):
        request.session['editing_client'] = None
        return redirect('/mailing/clients/create/')


class ClientListView(ListView):
    model = Client
    queryset = Client.objects.all()


class ClientDeleteView(DeleteView):
    model = Client
    success_url = '/mailing/clients/create/'

class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = '/mailing/messages/'

class MessageListView(ListView):
    model = Message
    queryset = Message.objects.all()

class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = '/mailing/messages/'

class MessageDeleteView(DeleteView):
    model = Message
    success_url = '/mailing/messages/'

class MailingCreateView(View):
    def get(self, request):
        form = MailingForm()
        return render(request, 'mailing/mailing_form.html', {'form': form})

    def post(self, request):
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.status = "Создана"
            mailing.save()
            form.save_m2m()  # Сохраняем многие-ко-многим отношения
            return redirect('/mailing/mailings/')
        return render(request, 'mailing/mailing_form.html', {'form': form})

class MailingListView(ListView):
    model = Mailing
    queryset = Mailing.objects.all()
    template_name = 'mailing/mailing_form.html'

class MailingRepeatView(View):
    def get(self, request, pk):
        mailing = Mailing.objects.get(pk=pk)
        # Логика повторной отправки рассылки
        return redirect('/mailing/mailings/')

class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = '/mailing/mailings/'

class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = '/mailing/mailings/'

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
    # Проверка прав доступа
    if not request.user.is_staff:
        return HttpResponseForbidden("Доступ запрещен")

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
    return redirect('/mailing/mailings/')
