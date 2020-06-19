from django.urls import path

from . import views

app_name = 'profiler'
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('load_test', views.IndexView.as_view(), name='home'),
    path('create_database_profile', views.create_database_profile),
    path('check_progress/<int:db_profile_id>', views.check_progress),
    path('database_profile/<int:db_profile_id>', views.database_profile, name='database_profile'),
    path('load_test_start/<int:test_id>', views.load_test_start),
    path('load_test_check/<int:test_id>', views.load_test_check),
]
