import secrets
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, CreateView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет! Перейди по ссылки для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.token = None
    user.save()
    return redirect(reverse("users:login"))

def manager_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.role == 'manager')(view_func)

@manager_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

@manager_required
def block_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = False
    user.save()
    return redirect('users:user_list')

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_form.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user

    def get_form_class(self):
        print("Используемая форма:", self.form_class)
        return super().get_form_class()
