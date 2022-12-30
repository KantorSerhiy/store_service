from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control py-4",
                "placeholder": "Input username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control py-4",
                "placeholder": "Input password",
            }
        )
    )

    class Meta:
        model = User
        fields = ["username", "password"]


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control py-4",
                "placeholder": "input you First name"
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control py-4",
                "placeholder": "input you Last name"
            }
        )
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control py-4",
                "placeholder": "input you username"
            }
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control py-4",
                "placeholder": "input you email"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control py-4",
                "placeholder": "input you password"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control py-4",
                "placeholder": "confirm you password"
            }
        )
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4"}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4"}), required=False)
    image = forms.ImageField(widget=forms.FileInput(attrs={"class": "custom-file-input"}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4", "readonly": True}))
    email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4", "readonly": True}))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "image", "username", "email"]
