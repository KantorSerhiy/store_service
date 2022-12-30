from django.contrib import auth
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

from users.forms import UserLoginForm, UserRegisterForm


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


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:login")
    else:
        form = UserRegisterForm
    context = {
        "form": form
    }
    return render(request, "users/register.html", context=context)