from django.contrib import auth, messages
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from products.models import Basket
from users.models import User


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("index")


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def get_context_data(self, **kwargs):
        context = super(UserRegisterView, self).get_context_data()
        context["title"] = "Store - Registration"
        return context


class UserProfileView(UpdateView):
    model = User  # TODO: add success massage for update profile
    form_class = UserProfileForm
    template_name = "users/profile.html"

    def get_success_url(self):
        return reverse_lazy("users:profile", args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context["title"] = "Store - Profile"
        context["basket"] = Basket.objects.filter(user=self.object)
        return context


def logout(request):
    auth.logout(request)
    return redirect("index")
