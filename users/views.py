from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView

from common.views import TitleMixin
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from products.models import Basket
from users.models import User, EmailVerification


class UserLoginView(TitleMixin, LoginView):
    template_name = "users/login.html"
    title = "Store - Login"
    form_class = UserLoginForm
    success_url = reverse_lazy("index")


class UserRegisterView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    title = "Store - Registration"
    success_url = reverse_lazy("users:login")
    success_message = "Gratz, you are successful register"


class UserProfileView(TitleMixin, UpdateView):
    model = User  # TODO: add success massage for update profile
    form_class = UserProfileForm  # TODO: look to update
    template_name = "users/profile.html"
    title = "Store - Profile"

    def get_success_url(self):
        return reverse_lazy("users:profile", args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context["basket"] = Basket.objects.filter(user=self.object)
        return context


def logout(request):
    auth.logout(request)
    return redirect("index")


class EmailVerificationView(TitleMixin, TemplateView):
    title = "Store - confirm email"
    template_name = "users/email_verification.html"

    def get(self, request, *args, **kwargs):
        code = kwargs["code"]
        user = User.objects.get(email=kwargs["email"])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("index"))
