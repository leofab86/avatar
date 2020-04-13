from django.urls import path

from . import views

app_name = 'profiler'
urlpatterns = [
    path('', views.home, name='home'),
]
