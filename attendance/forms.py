from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from attendance.models import Attendance, meetAlert

from django.db import transaction

class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        exclude = ['username']
        fields = '__all__'


# class EmployeeSignUpForm(UserCreationForm):
#
#     class Meta(UserCreationForm.Meta):
#         model = User
#
#     @transaction.atomic
#     def save(self):
#         user = super().save(commit=False)
#         user.is_employee = True
#         user.save()
#         student = Employee.objects.create(user=user)
#
#         return user


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


class MeetForm(ModelForm):
    class Meta:
        model = meetAlert
        fields = '__all__'
