from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test


class Cars(models.Model):
    manufacturer = models.CharField("Производитель", max_length=30)
    model = models.CharField("Модель", max_length=100, unique=True)
    
    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        
    def __str__(self):
        return str(self.manufacturer) + ' ' + str(self.model)


class DescriptionCar(models.Model):
    car = models.OneToOneField(Cars, on_delete=models.CASCADE, verbose_name="Автомобиль", unique=True)
    description = models.TextField("Описание")

    class Meta:
        verbose_name = "Описание автомобиля"
        verbose_name_plural = "Описание автомобиля"

    def __str__(self):
        return str(self.car)


class Service(models.Model):
    title = models.CharField(max_length=30, unique=True, verbose_name="Услуга")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.title


class CategoryJob(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")
    title = models.CharField("Категория работ", max_length=30, unique=True)

    class Meta:
        verbose_name = "Категория работ"
        verbose_name_plural = "Категории работ"

    def __str__(self):
        return str(self.title)


class DescriptionCategoryJob(models.Model):
    category_job = models.OneToOneField(CategoryJob, on_delete=models.CASCADE, verbose_name="Категория работ")
    description = models.TextField("Описание")

    class Meta:
        verbose_name = "Описание"
        verbose_name_plural = "Описание"

    def __str__(self):
        return str(self.category_job)


class DescriptionCategoryForCar(models.Model):
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, verbose_name="Автомобиль")
    category_job = models.ForeignKey(CategoryJob, on_delete=models.CASCADE, verbose_name="Категория работ")
    description = models.TextField("Описание", unique=True)

    class Meta:
        verbose_name = "Описание работы"
        verbose_name_plural = "Описание работ"

    def __str__(self):
        return str(self.car) + ' ' + str(self.category_job)


class Jobs(models.Model):
    title = models.CharField("Работа", max_length=100)
    hour_norm = models.FloatField("Нормо-час", max_length=10)
    price_per_hour = models.FloatField("Цена за час", max_length=10)
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, blank=True, verbose_name="Автомобиль")
    category_job = models.ForeignKey(CategoryJob, on_delete=models.CASCADE, verbose_name="Категория работ")
    
    class Meta:
        verbose_name = "Работа"
        verbose_name_plural = "Работы"

    def __str__(self):
        return self.title + ' ' + str(self.car)
        

class Employees(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name="Сотрудник")
    phone_number = PhoneNumberField("Номер телефона")
    name = models.CharField("Имя", max_length=50)
    surname = models.CharField("Фамилия", max_length=50)
    patronymic = models.CharField("Отчество", max_length=50, blank=True)
    birth_date = models.DateField("Дата рождения", blank=True)
    passport = models.CharField("Серия и номер паспорта", max_length=10)
    location = models.CharField("Адрес", max_length=100, blank=True)
    job = models.ManyToManyField(Jobs, blank=True)
    
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ['surname']

    def __str__(self):
        return self.surname + ' ' + self.name

    def display_group(self):
        groups = []
        results = User.objects.get(id=self.user_id).groups.all()
        for group in results:
            groups.append(group)
        return groups
    display_group.short_description = 'Группа'
        

class Clients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = PhoneNumberField("Номер телефона", )
    name = models.CharField("Имя",  max_length=50)
    surname = models.CharField("Фамилия", max_length=50)
    patronymic = models.CharField("Отчество", max_length=50, blank=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['surname']

    def __str__(self):
        return self.surname + ' ' + self.name


class ClientCars(models.Model):
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, verbose_name="Автомобиль")
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    distance = models.FloatField("Пробег")
    year_of_manufacture = models.DateField("Год выпуска")
    numberplate = models.CharField("Номерной знак", max_length=9)
    
    class Meta:
        verbose_name = "Автомобиль клиента"
        verbose_name_plural = "Автомобили клиентов"

    def __str__(self):
        return str(self.car)
    

class Orders(models.Model):
    client_car = models.ForeignKey(ClientCars, on_delete=models.CASCADE, verbose_name="Автомобиль")
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, verbose_name="Клиент")
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, verbose_name="Сотрудник")
    status = models.BooleanField("Статус заказа", default=0)
    registration_date = models.DateTimeField("Дата оформления")
    execution_date = models.DateTimeField("Дата исполнения")
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return str(self.client) + ' ' + str(self.client_car)


class DetailOrders(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name="Заказ")
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, verbose_name="Сотрудник")
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, verbose_name="Работа")
    status = models.BooleanField("Статус заказа", default=0)
    registration_date = models.DateTimeField("Дата оформления")
    execution_date = models.DateTimeField("Дата исполнения")
    number = models.IntegerField("Количество", default=1)
    total = models.FloatField("Итого", default=1)
    
    class Meta:
        verbose_name = "Работа"
        verbose_name_plural = "Необходимые работы"

    def __str__(self):
        return str(self.order)


def sidebar_service():
    category = {}
    ser = Service.objects.all()
    x = CategoryJob.objects.all()
    for i in ser:
        y = []
        for j in x:
            if i.id == j.service_id:
                y.append({j.id: j.title})
        if y:
            category[i.title] = y
        else:
            category[i.title] = [{'null': 'Нет данных'}]
    return category


def sidebar_car():
    category = {}
    car = Cars.objects.all()
    x = DescriptionCar.objects.all()
    for i in car:
        y = []
        for j in x:
            if j.car.manufacturer == i.manufacturer:
                y.append({j.id: j.car.model})
        if y:
            category[i.manufacturer] = y
    return category


def sidebar_service_car(pk):
    category = {}
    ser = Service.objects.all()
    x = CategoryJob.objects.all()
    s = DescriptionCategoryForCar.objects.filter(car_id=pk)
    for i in ser:
        y = []
        for j in x:
            if i.id == j.service_id:
                for m in s:
                    if m.category_job_id == j.id:
                        y.append({m.id: j.title})
        if y:
            category[i.title] = y
        else:
            category[i.title] = [{'null': 'Нет данных'}]
    return category


def group_required(*group_names):
    def in_groups(user):
        if user.is_superuser or bool(user.groups.filter(name__in=group_names)):
            return True
        return False
    return user_passes_test(in_groups)
