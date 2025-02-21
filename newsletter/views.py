from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Recipient


def home_page(request):
    return render(request, 'home_page.html')

def recipient_list(request):
    recipients = Recipient.objects.all()
    return render(request, 'newsletter/recipient_list.html', {'recipients': recipients})


def recipient_add(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        comment = request.POST.get('comment')

        Recipient.objects.create(email=email, full_name=full_name, comment=comment)
        return redirect(reverse('newsletter:recipient_list'))

    return render(request, 'newsletter/recipient_form.html')


def recipient_edit(request, pk):
    recipient = get_object_or_404(Recipient, pk=pk)
    if request.method == 'POST':
        recipient.email = request.POST.get('email')
        recipient.full_name = request.POST.get('full_name')
        recipient.comment = request.POST.get('comment')
        recipient.save()
        return redirect(reverse('newsletter:recipient_list'))

    return render(request, 'newsletter/recipient_form.html', {'recipient': recipient})


def recipient_delete(request, pk):
    recipient = get_object_or_404(Recipient, pk=pk)
    if request.method == 'POST':
        recipient.delete()
        return redirect(reverse('newsletter:recipient_list'))

    return render(request, 'newsletter/recipient_confirm_delete.html', {'recipient': recipient})
