from django.urls import path

from . import views

app_name = 'portfolio'
urlpatterns = [
    path('', views.home, name='home'),
    path('details/<int:project_id>', views.details, name='details')
]
