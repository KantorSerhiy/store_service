from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from products.models import Basket
from users.models import User


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("/")

    else:
        form = UserLoginForm()
    context = {
        "form": form
    }
    return render(request, "users/login.html", context=context)


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
