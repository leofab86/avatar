from django.urls import path

from . import views

app_name = 'profiler'
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('create_database_profile', views.create_database_profile),
    path('check_progress/<int:db_profile_id>', views.check_progress),
    path('database_profile/<int:db_profile_id>', views.database_profile, name='database_profile'),
    path('load_test_start/<int:test_id>', views.load_test_start),
    path('load_test_check/<int:test_id>/<str:batch>', views.load_test_check),
    path('preview/ssr', views.LoadTestSSRPreview.as_view(), name='preview_ssr'),
    path('preview/spa', views.LoadTestSPAPreview.as_view(), name='preview_spa'),
    path('check_user_status', views.check_stack),
    path('check_user_status_and_restart', views.check_stack_and_restart),
    path('turn_off_stack', views.check_stack_and_turn_off)
]
