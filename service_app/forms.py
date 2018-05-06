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


class ClientCarForm(forms.ModelForm):
    year_of_manufacture = forms.DateField(widget=forms.SelectDateWidget(years=range(1990, 2018)), label="Дата производства")

    class Meta:
        model = ClientCars
        fields = ('car', 'distance', 'year_of_manufacture', 'numberplate')


class JobsForm(forms.Form):
    choices = forms.ModelMultipleChoiceField(queryset=Jobs.objects.none(), required=True, widget=forms.CheckboxSelectMultiple)

    def __init__(self, car):
        super(JobsForm, self).__init__()
        self.fields['choices'].queryset = Jobs.objects.filter(car=car)


class OrderForm(forms.ModelForm):
    registration_date = forms.DateTimeField(widget=forms.SelectDateWidget, label='Дата посещения')

    def __init__(self, pk, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['client_car'].queryset = ClientCars.objects.filter(client_id=int(pk))

    class Meta:
        model = Orders
        fields = ('client_car', 'registration_date')


class CalcForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = ('car',)


class ColForm(forms.Form):
    col = forms.IntegerField(widget=forms.NumberInput, initial=1, min_value=1, max_value=20)
