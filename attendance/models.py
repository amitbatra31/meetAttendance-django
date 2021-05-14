from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from datetime import date,time
from django.utils import timezone
# from .views import my_view
# Create your models here.


# class User(AbstractUser):
#     is_admin = models.BooleanField(default = False)
#     is_employee = models.BooleanField(default = False)
#
# class Employee(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    date = models.DateField(default = timezone.now)


class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    presence = models.CharField(max_length=50)


class Attendance(models.Model):
    # first_name = models.CharField(max_length = 200)
    # username = models.CharField(max_length = 200)
    username = models.CharField(max_length = 200,primary_key=True)
    Date = models.DateField(default = date.today)
    Time = models.TimeField(default = timezone.now)
    Present = models.BooleanField(default = False)
    def __str__(self):
        return '%s' % self.username


class meetAlert(models.Model):
    agenda = models.CharField(max_length = 200)
    venue = models.CharField(max_length = 200)
    Date = models.DateField()
    Time = models.TimeField()
    permissions = 'can_add'
    # slug = models.SlugField(unique=True)

    def __str__(self):
        return self.agenda
