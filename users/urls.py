from django.urls import path

from users.views import login, register, profile

urlpatterns = [
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
]


app_name = "users"
