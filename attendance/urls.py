from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.index, name = 'index'),
    path('dashboard',TemplateView.as_view(template_name="base.html")),

]