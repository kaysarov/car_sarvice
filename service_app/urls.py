"""car_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [path('', views.home, name='home'),
               path('sign_up', views.sign_up, name='sign_up'),
               path('services', views.services, name='services'),
               path('service/<pk>/', views.service, name='service'),
               path('car/desc/<car>/<pk>/', views.car_desc, name='car_desc'),
               path('car/<pk>/', views.car, name='car'),
               path('appointment', views.appointment, name='appointment')
               ]
