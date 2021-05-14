from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import meetAlert, Attendance
from .forms import AttendanceForm, SignupForm, MeetForm
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import unauthenticated_user, allowed_users
from django.http import JsonResponse
from django.core import serializers
import matplotlib.pyplot as plt
import numpy as np
import io
import urllib, base64
from django.contrib.auth.decorators import login_required

# @unauthenticated_user

# def index(request):
#     form = CustomerForm()
#     context = {'form': form}
#     if request.method == 'POST':
#         print(request.POST)
#         form = CustomerForm(request.POST)
#         if form.is_valid():
#             form.save()
#     return render(request, "index.html", context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'common/change_password.html', {
        'form': form
    })




class HomeView(TemplateView):
    template_name = 'common/home.html'


# class AddMeetView(CreateView):
#     form_class = MeetForm
#     success_url = reverse_lazy('home')
#     template_name = 'common/add-meet.html'


class SignUpView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('home')
    template_name = 'common/register.html'


class BaseView(LoginRequiredMixin,TemplateView):
    template_name = 'base.html'
    login_url = reverse_lazy('home')


def my_view(request):
    username = request.user.get_username()
    first_name = request.user.get_short_name()


def add_attendance(request):
    form = AttendanceForm()
    context = {'form': form}
    if request.method == 'POST':
        print(request.POST)
        form = AttendanceForm(request.POST)

        if form.is_valid():
            # form.save(commit=False)
            form.instance.username = request.user
            if Attendance.objects.filter(pk=request.user).exists():
                Attendance.objects.filter(pk=request.user).update(Present=True)
            # form.username = request.user
            # print(request.user.get_username())
            # form.first_name = request.user.get_short_name()
            form.save()



    return render(request, "common/add-attendance.html", context)


class MeetDetailView(LoginRequiredMixin, ListView):
    model = meetAlert
    template_name = 'common/meet-reminders.html'
    queryset = meetAlert.objects.all()
    # def get_context_data(self, **kwargs):
    #     context = super(MeetDetailView, self).get_context_data(**kwargs)
    #     context['agenda'] = meetAlert.objects.all()
    #     return context


class AttendanceDetailView(LoginRequiredMixin, TemplateView):
    model = Attendance
    template_name = 'common/dashboard.html'
    p = Attendance.objects.all().filter(Present=True)
    q = Attendance.objects.all().filter(Present=False)
    # def get_context_data(self, **kwargs):
    #     context = super(AttendanceDetailView, self).get_context_data(**kwargs)
    #     context['Present'] = Attendance.objects.all()
    #     return context


def attendanceDetail(request):
    p = Attendance.objects.all().filter(Present = True)
    q = Attendance.objects.all().filter(Present = False)
    total = Attendance.objects.all().count()
    meet = meetAlert.objects.all().count()
    #MATPLOTLIB pie
    y= np.array([int(p.count()),int(q.count())])
    mylabels = ['Present', 'Absent']
    plt.pie(y,labels = mylabels)
    # Passing pie chart as buffer
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf,format= 'png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
     # Sending all data as dictionary
    context = {'p':p,'q':q,'total': total,'meet':meet, 'data':uri}

    return render(request, 'common/dashboard.html', context)
# @login_required(login_url='login')

@allowed_users(allowed_roles = ['admin'])
def add_meet(request):
    form = MeetForm()
    context = {'form': form}
    if request.method == 'POST':
        print(request.POST)

        form = MeetForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, "common/add-meet.html", context)

class DashboardView(LoginRequiredMixin,PermissionRequiredMixin, TemplateView):
    template_name = 'common/dashboard.html'
    login_url = reverse_lazy('home')
    permission_required = 'meetAlert.can_add'



