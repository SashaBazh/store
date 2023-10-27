from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm, UserProfile2Form
from users.models import EmailVerification, User


class UserLoginView(LoginView):
    template_name = 'users/login_2.html'
    form_class = UserLoginForm
    title = 'Магазин - Авторизация'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration_2.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегестрировались!'
    title = 'Магазин - Регистрация'


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class UserProfile2View(TitleMixin, UpdateView):
    model = User
    form_class = UserProfile2Form
    template_name = 'users/basket.html'
    title = 'Store - Корзина'

    def get_success_url(self):
        return reverse_lazy('users:basket', args=(self.object.id,))


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Магазин - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists(): # and not email_verifications.first().is_expired:
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
