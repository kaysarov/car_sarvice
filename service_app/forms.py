from django import forms
from service_app.models import *


class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, label="Логин", min_length=3)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(), label="Пароль", min_length=8)

    class Meta:
        model = User
        fields = ('username', 'password')


class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ('name', 'surname', 'patronymic', 'phone_number')


