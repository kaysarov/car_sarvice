from django.shortcuts import render


def home(request):
    return render(request, 'service_app/index.html', {})
