from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Client, Message, Mailing
from .forms import ClientForm, MessageForm, MailingForm
from django.core.mail import send_mail
from django.utils import timezone
from django.shortcuts import get_object_or_404


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
    messages_count = Message.objects.count()

    context = {
        'clients_count': clients_count,
        'messages_count': messages_count,
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
        mailing.save()
        form.save_m2m()  # Сохраняем многие-ко-многим отношения
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


def send_mailing(mailing_id):
    mailing = Mailing.objects.get(pk=mailing_id)

    # Логика отправки рассылки
    for client in mailing.clients.all():
        send_mail(
            subject=mailing.message.topic_message,
            message=mailing.message.text_message,
            from_email='your_email@example.com',  # Замените на ваш email
            recipient_list=[client.email],
        )

    # Обновление статуса рассылки
    if mailing.end_date and mailing.end_date < timezone.now().date():
        mailing.status = 'Завершена'
        mailing.save()


def send_mailing_post(request, pk):
    if request.method == 'POST':
        mailing = get_object_or_404(Mailing, pk=pk)
        # Логика отправки рассылки
        for client in mailing.clients.all():
            send_mail(
                subject=mailing.message.topic_message,
                message=mailing.message.text_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email],
            )
        mailing.status = 'Запущена'
        mailing.save()
        return redirect('/mailing/mailings/')
    return redirect('/mailing/mailings/')