from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from products.models import Basket


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
            messages.success(request, "Grats, you have successfully registered. Now - log in!")
            return redirect("users:login")
    else:
        form = UserRegisterForm
    context = {
        "form": form
    }
    return render(request, "users/register.html", context=context)


@login_required
def profile(request):  # TODO: add success massage for update profile
    if request.method == "POST":
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("users:profile")
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)

    baskets = Basket.objects.filter(user=request.user)

    context = {
        "title": "Profile",
        "form": form,
        "basket": baskets,
    }
    return render(request, "users/profile.html", context=context)


def logout(request):
    auth.logout(request)
    return redirect("index")
