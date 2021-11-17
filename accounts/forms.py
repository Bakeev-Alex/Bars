from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import (password_validation)

from .models import Student, Professor


password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'field__input', 'placeholder': 'Введите пароль', 'required': True},),
        help_text=password_validation.password_validators_help_text_html())
password2 = forms.CharField(widget=forms.PasswordInput(
    attrs={'class': 'field__input', 'placeholder': 'Подтвердите пароль', 'required': True}))


class AuthenticationUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'field__input', 'placeholder': 'Введите ваш логин', 'required': True, 'type': 'text'}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'field__input', 'placeholder': 'Введите ваш пароль', 'required': True}),
    )


class StudentForm(UserCreationForm):

    password1 = password1
    password2 = password2

    class Meta:
        model = Student
        fields = ['username',
                  'first_name', 'last_name',
                  'password1', 'password2', 'study_group']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'field__input', 'placeholder': 'Введите пользователя', 'required': True}, ),
            'first_name': forms.TextInput(
                attrs={'class': 'field__input', 'placeholder': 'Введите имя', 'required': True}, ),
            'last_name': forms.TextInput(
                attrs={'class': 'field__input', 'placeholder': 'Введите фамилию', 'required': True}, ),
            'study_group': forms.Select(attrs={'class': 'field__input', 'placeholder': 'Выберите группу', 'required': True})
        }


class ProfessorForm(UserCreationForm):
    password1 = password1
    password2 = password2

    class Meta:
        model = Professor
        fields = ['username',
                  'first_name', 'last_name',
                  'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'field__input', 'placeholder': 'Введите пользователя', 'required': True},),
            'first_name': forms.TextInput(attrs={'class': 'field__input', 'placeholder': 'Введите имя', 'required': True},),
            'last_name': forms.TextInput(attrs={'class': 'field__input', 'placeholder': 'Введите фамилию', 'required': True},),
        }