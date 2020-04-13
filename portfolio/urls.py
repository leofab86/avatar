from django.urls import path

from . import views

app_name = 'reactserver'
urlpatterns = [
    path('', views.home, name='home'),
    path('details/<int:project_id>', views.details, name='details')
]
