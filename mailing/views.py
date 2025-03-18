from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Client, Message, Mailing, Attempt
from .forms import ClientForm, MessageForm, MailingForm
from django.core.mail import send_mail
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import datetime


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


class MessageCreateView(View):
    def get(self, request):
        form = MessageForm()
        messages = Message.objects.all().order_by('id')
        editing_message = request.session.get('editing_message', None)
        return render(request, 'mailing/text_form.html', {'form': form, 'messages': messages, 'editing_message': editing_message})

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.path)
        messages = Message.objects.all().order_by('id')
        editing_message = request.session.get('editing_message', None)
        return render(request, 'mailing/text_form.html', {'form': form, 'messages': messages, 'editing_message': editing_message})


class MessageEditView(View):
    def get(self, request, pk):
        request.session['editing_message'] = pk
        return redirect('/mailing/messages/create/')

class MessageSaveView(View):
    def post(self, request, pk):
        message = Message.objects.get(pk=pk)
        message.topic_message = request.POST.get('topic_message', message.topic_message)
        message.text_message = request.POST.get('text_message', message.text_message)
        message.save()
        request.session['editing_message'] = None
        return redirect('/mailing/messages/create/')

class MessageCancelView(View):
    def get(self, request, pk):
        request.session['editing_message'] = None
        return redirect('/mailing/messages/create/')

class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = '/mailing/messages/'

class MessageDeleteView(DeleteView):
    model = Message
    success_url = '/mailing/messages/create/'  # Перенаправляем на страницу с формой


def index(request):
    clients_count = Client.objects.count()
    mailings_count = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status='Запущена').count()

    context = {
        'clients_count': clients_count,
        'mailings_count': mailings_count,
        'active_mailings': active_mailings,
    }
    return render(request, 'mailing/index.html', context)


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = '/mailing/mailings/'  # Перенаправляем на список рассылок

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.status = "Создана"

        if mailing.repeat == 'once':
            mailing.end_datetime = mailing.start_datetime
        else:
            # Присвоение времени из даты начала
            mailing.end_datetime = datetime.datetime.combine(
                mailing.end_datetime.date(),
                mailing.start_datetime.time()
            )
        mailing.save()
        form.save_m2m()
        return super().form_valid(form)

class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'

class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = '/mailing/mailings/'

class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = '/mailing/mailings/'


def send_mailing_post(request, pk):
    if request.method == 'POST':
        mailing = get_object_or_404(Mailing, pk=pk)

        mailing.status = 'Запущена'
        mailing.save()

        # Отправка рассылки с сохранением попыток
        for client in mailing.clients.all():
            try:
                send_mail(
                    subject=mailing.message.topic_message,
                    message=mailing.message.text_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                )
                Attempt.objects.create(
                    mailing=mailing,
                    client=client,
                    status='success',
                    server_response='Успешно'
                )
            except Exception as e:
                Attempt.objects.create(
                    mailing=mailing,
                    client=client,
                    status='failed',
                    server_response=str(e)
                )

        # Проверка статуса рассылки
        if mailing.repeat == 'once':
            if mailing.start_datetime < timezone.now():
                mailing.status = 'Завершена'
                mailing.save()
        else:
            if mailing.end_datetime is not None and mailing.end_datetime < timezone.now():
                mailing.status = 'Завершена'
                mailing.save()

        return redirect('/mailing/mailings/')
    return redirect('/mailing/mailings/')


class StatisticsView(View):
    def get(self, request):
        successful_attempts = Attempt.objects.filter(status='success').count()
        failed_attempts = Attempt.objects.filter(status='failed').count()
        last_attempts = Attempt.objects.order_by('-attempt_datetime')[:10]

        context = {
            'successful_attempts': successful_attempts,
            'failed_attempts': failed_attempts,
            'last_attempts': last_attempts,
        }
        return render(request, 'mailing/statistics.html', context)
