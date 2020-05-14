from django.urls import path

from . import views

app_name = 'profiler'
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('create_database_profile', views.create_database_profile),
    path('check_progress/<int:db_profile_id>', views.check_progress),
    path('delete_database_profile/<int:db_profile_id>', views.delete_database_profile),
]
