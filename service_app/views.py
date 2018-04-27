from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login
from .models import *


def home(request):
    return render(request, 'service_app/index.html', {})


def sign_up(request):
    user_form = UserForm()
    client_form = ClientForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        client_form = ClientForm(request.POST)
        group = Group.objects.get(name='client')
        if user_form.is_valid() and client_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_client = client_form.save(commit=False)
            new_client.user_id = new_user.id
            new_client.save()
            group.user_set.add(new_user.id)
            login(request, authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password']
            ))
            return redirect(home)
    return render(request, 'registration/sign_up.html', {
        'user_form': user_form,
        'client_form': client_form
    })

def services(request):
    category = sidebar_service()
    cars = sidebar_car()
    return render(request, 'service_app/services.html', {'services': category, 'cars': cars})


def service(request, pk):
    service = sidebar_service()
    desc = get_object_or_404(DescriptionCategoryJob, category_job_id=pk)
    return render(request, 'service_app/service.html', {'services': service, 'desc': desc})


def car(request, pk):
    category = sidebar_service_car(pk)
    desc = get_object_or_404(DescriptionCar, car_id=pk)
    return render(request, 'service_app/car_desc.html', {'services': category, 'desc': desc, 'car': pk})


def car_desc(request, car, pk):
    category = sidebar_service_car(car)
    desc = get_object_or_404(DescriptionCategoryForCar, id=pk)
    return render(request, 'service_app/car_desc.html', {'services': category, 'desc': desc, 'car': car})


def appointment(request):
    return render(request, 'service_app/appointment.html', {})


#@group_required('client', 'master')
