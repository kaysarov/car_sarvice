from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin, SummernoteInlineModelAdmin


class Jobs(admin.TabularInline):
    model = Jobs
    extra = 0
    list_display = ('title', 'hour_norm', 'price_per_hour', 'car', 'category_job')
    list_filter = ('category_job',)


class DetailOrders(admin.TabularInline):
    model = DetailOrders
    extra = 0
    fields = ('order', 'job', 'employee', 'registration_date', 'execution_date', 'status', 'number')


class ClientCars(admin.TabularInline):
    model = ClientCars
    extra = 0
    list_display = ('client', 'car', 'numberplate', 'year_of_manufacture', 'distance')
    list_filter = ('client', 'car')


class DescriptionCar(admin.StackedInline, SummernoteInlineModelAdmin):
    model = DescriptionCar
    list_display = ('car', 'description')


class DescriptionCategoryJob(admin.StackedInline, SummernoteInlineModelAdmin):
    model = DescriptionCategoryJob
    list_display = ('category_job',)


class DescriptionCategoryForCar(admin.TabularInline, SummernoteInlineModelAdmin):
    model = DescriptionCategoryForCar
    extra = 0
    list_display = ('car', 'category_job')
    list_filter = ('car', 'category_job')


@admin.register(Cars)
class Cars(admin.ModelAdmin):
    list_display = ('manufacturer', 'model')
    list_filter = ('manufacturer',)
    inlines = [DescriptionCar, DescriptionCategoryForCar]


@admin.register(Clients)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'patronymic', 'phone_number')
    inlines = [ClientCars]


@admin.register(Employees)
class EmpoyeeAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'phone_number', 'display_group')


@admin.register(Service)
class Service(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(CategoryJob)
class CategoryJob(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [DescriptionCategoryJob, Jobs]


@admin.register(Orders)
class Orders(admin.ModelAdmin):
    fields = ['status', 'client', 'client_car', ('registration_date', 'execution_date'), 'employee']
    list_display = ('status', 'client', 'client_car', 'registration_date', 'employee')
    list_filter = ('status', 'employee')
    inlines = [DetailOrders]
