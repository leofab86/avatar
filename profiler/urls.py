from django.urls import path

from . import views

app_name = 'profiler'
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('create_database_profile', views.create_database_profile),
    path('delete_database_profile', views.delete_database_profile)
]
