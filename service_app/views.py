from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login
from .models import *
from django.contrib.auth.views import password_change, password_change_done
from django.http import Http404


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


def home(request):
    return render(request, 'service_app/index.html', {})


def services(request):
    category = sidebar_service()
    cars = sidebar_car()
    return render(request, 'service_app/services.html', {'services': category, 'cars': cars})


def service(request, pk):
    category = sidebar_service()
    desc = get_object_or_404(DescriptionCategoryJob, category_job_id=pk)
    return render(request, 'service_app/service.html', {'services': category, 'desc': desc})


def car(request, pk):
    category = sidebar_service_car(pk)
    desc = get_object_or_404(DescriptionCar, car_id=pk)
    return render(request, 'service_app/car_desc.html', {'services': category, 'desc': desc, 'car': pk})


def car_desc(request, car, pk):
    category = sidebar_service_car(car)
    desc = get_object_or_404(DescriptionCategoryForCar, id=pk)
    price = price_list(car, pk)
    return render(request, 'service_app/price.html', {'services': category, 'desc': desc, 'car': car, 'price': price})


def calc(request):
    form = CalcForm()
    if request.method == 'POST':
        form = CalcForm(request.POST)
        if form.is_valid():
            car = request.POST['car']
            choices = JobsForm(car)
            col = ColForm()
            job = Jobs.objects.filter(car_id=car)
            for i in range(len(job)):
                for j in choices:
                    job[i].choices = j[i]
                    for x in col:
                        job[i].col = x
            return render(request, 'service_app/calc.html', {'form': form, 'job': job, 'car': car})
    return render(request, 'service_app/calc.html', {'form': form})


def calc_done(request, pk):
    job, sum, time = calculate(request, pk)
    return render(request, 'service_app/calc_done.html', {'job': job, 'sum': sum, 'time': time})


@group_required('client')
def lk(request, pk):
    if request.user.id == int(pk):
        cars = ClientCars.objects.filter(client_id=pk)
        return render(request, 'service_app/lk_content.html', {'pk': pk, 'cars': cars})
    raise Http404()


@group_required('client')
def edit_profile(request, pk):
    if request.user.id == int(pk):
        client_form = ClientForm(instance=Clients.objects.get(user_id=pk))
        if request.method == 'POST':
            client_form = ClientForm(request.POST, instance=Clients.objects.get(user_id=pk))
            if client_form.is_valid():
                client = client_form.save()
        return render(request, 'service_app/lk_edit_profile.html', {'form': client_form, 'pk': pk})
    raise Http404()


def change_password(request):
    return password_change(request, template_name='registration/change_password.html')


def password_change_done(request):
    return password_change(request, template_name='registration/password_done.html')


@group_required('client')
def add_car(request, pk):
    if request.user.id == int(pk):
        client_car_form = ClientCarForm()
        if request.method == 'POST':
            client_car_form = ClientCarForm(request.POST)
            if client_car_form.is_valid():
                a = client_car_form.save(commit=False)
                a.client_id = pk
                a.save()
                return redirect(lk, pk)
        return render(request, 'service_app/lk_add_car.html', {'form': client_car_form, 'pk': pk})
    raise Http404()


@group_required('client')
def edit_car(request, pk, car):
    if request.user.id == int(pk):
        client_car_form = ClientCarForm(instance=ClientCars.objects.get(id=car))
        if request.method == 'POST':
            client_car_form = ClientCarForm(request.POST, instance=ClientCars.objects.get(id=car))
            if client_car_form.is_valid():
                a = client_car_form.save()
                return redirect(lk, pk)
        return render(request, 'service_app/lk_edit_car.html', {'form': client_car_form, 'pk': pk, 'car': car})
    raise Http404()


@group_required('client')
def del_car(request, pk, car):
    if request.user.id == int(pk):
        a = ClientCars(id=car)
        a.delete()
        return redirect(lk, pk)
    raise Http404()


@group_required('client', 'master')
def appointment(request, pk):
    if request.user.id == int(pk):
        order = OrderForm(pk)
        if request.method == 'POST':
            order = OrderForm(pk, request.POST)
            if order.is_valid():
                a = order.save(commit=False)
                a.client_id = pk
                a.save()
                return redirect(orders, pk)
        return render(request, 'service_app/appointment.html', {'pk': pk, 'form': order})
    raise Http404()


@group_required('client', 'master')
def orders(request, pk):
    if request.user.id == int(pk):
        orders = Orders.objects.filter(client_id=pk)
        return render(request, 'service_app/lk_orders.html', {'pk': pk, 'orders': orders})
    raise Http404()


@group_required('client', 'master')
def orders_detail(request, pk, order):
    if request.user.id == int(pk):
        orders = DetailOrders.objects.filter(order_id=order)
        return render(request, 'service_app/lk_orders_detail.html', {'pk': pk, 'orders': orders, 'id': order})
    raise Http404()
