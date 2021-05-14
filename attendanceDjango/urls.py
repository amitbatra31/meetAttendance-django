"""attendanceDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from attendance.views import DashboardView, change_password, add_meet, MeetDetailView, BaseView, add_attendance,AttendanceDetailView
import notifications.urls

from django.views.generic import TemplateView
from attendance.views import HomeView, SignUpView,attendanceDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name ='home'),
    # path('attendance/', include('attendance.urls')),
    path('login/', auth_views.LoginView.as_view(template_name ='common/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(next_page = 'home'), name = 'logout'),
    # path('dashboard/', DashboardView.as_view(), name = 'dashboard'),
    # path('dashboard/', AttendanceDetailView.as_view(), name = 'dashboard'),
    path('dashboard/', attendanceDetail, name = 'dashboard'),

    path('home/', BaseView.as_view(), name = 'base'),
    path('register/', SignUpView.as_view(), name = 'register'),
    path('register/Employee', SignUpView.as_view(), name = 'register'),
    path('register/admin', SignUpView.as_view(), name = 'register'),
    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name = 'common/change_password.html',
        success_url ='/'),
        name='change-password'),
    # path('add-meet/', TemplateView.as_view(
    #     template_name='common/add-meet.html'),
    #      name='add-meet'),
    path('add-meet/', add_meet,
         name='add-meet'),
    path('attendance/', add_attendance, name='attendance'),
    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='common/password-reset/password_reset.html',
             subject_template_name='commons/password-reset/password_reset_subject.txt',
             email_template_name='commons/password-reset/password_reset_email.html',
             success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='common/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='common/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='common/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    # url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('meetrem/', MeetDetailView.as_view(), name='meet-detail'),
]
