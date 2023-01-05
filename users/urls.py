from django.contrib.auth.decorators import login_required
from django.urls import path

from users.views import (
    UserLoginView,
    UserRegisterView,
    UserProfileView,
    logout,
    EmailVerificationView,
)

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("profile/", login_required(UserProfileView.as_view()), name="profile"),
    path("logout/", logout, name="logout"),
    path(
        "verify/<str:email>/<uuid:code>/",
        EmailVerificationView.as_view(),
        name="verify_email",
    ),
]


app_name = "users"
