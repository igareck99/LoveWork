from django.db import models
from datetime import datetime, time
import django.utils.timezone as dt

class User(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=36, unique=True)
    password = models.CharField(max_length=36, unique=True)
    tg_chat_id = models.IntegerField(default = None)
    def __str__(self):
        return '{}'.format(self.name)


class User_guest(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=69)
    b_date = models.DateField(null=True)
    phone = models.CharField(max_length=12, unique=True)
    session_password = models.CharField(max_length=16, unique=True)
    role = models.IntegerField(default=2)
    bonus_amount = models.IntegerField(default=0)
    reg_date = models.DateTimeField(default=dt.now)

    def __str__(self):
        return '{}'.format(self.name)


class Workshop(models.Model):
    id = models.AutoField(primary_key=True)
    workshop_id = models.IntegerField(default=id)
    workshop_name = models.CharField(default='Кухня', max_length=100)

class Food_class(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=49)
    parent_id = models.IntegerField(default=0)
    category_photo = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=49)
    price = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    photo = models.CharField(max_length=200, default='')
    parent_id = models.CharField(default=0, max_length=10)
    food_class = models.ForeignKey(Food_class, on_delete=models.CASCADE, null=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{} {}  {}'.format(self.food_class, self.name, self.price)


class Tables(models.Model):
    id = models.AutoField(primary_key=True)
    table_num = models.CharField(max_length=100, default='0')
    table_title = models.CharField(max_length=100, default='Стол')
    person_amount = models.IntegerField(default=4)
    info = models.CharField(max_length=200, default='')


class Registaration_guest(models.Model):
    id = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=15)
    code = models.IntegerField()
    date = models.DateTimeField(default=dt.now)


class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    rate = models.IntegerField()
    user = models.ForeignKey(User_guest, on_delete=models.CASCADE)

    def __str__(self):
        return 'Оценка {} {}'.format(self.rate, self.name)


class Shedule(models.Model):
    id = models.AutoField(primary_key=True)
    visit_day = models.DateField(null=False, default=datetime(year=2020, day=1, month=1))
    visit_time = models.TimeField(null=True, default=time(hour=1, minute=0))
    approved = models.BooleanField(default=None)
    comment = models.CharField(default='', max_length=200, null=True)
    guest = models.ForeignKey(User_guest, on_delete=models.CASCADE, null=False)
    table = models.ForeignKey(Tables, on_delete=models.CASCADE)

    def __str__(self):
        return 'Гость {} записан '.format(self.guest.name)


class Admin_shedule(models.Model):
    id = models.AutoField(primary_key=True)
    work_date = models.DateField(null=False, default=datetime(year=2020, day=1, month=1))
    start_work_time = models.TimeField(null=True, default=time(hour=0, minute=1))
    end_work_time = models.TimeField(null=True, default=time(hour=23, minute=59))
    comment = models.CharField(max_length=200, default='', null=True)

    def __str__(self):
        return 'Дата {}'.format(self.work_date)






