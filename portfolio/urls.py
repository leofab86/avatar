from django.urls import path

from . import views

app_name = 'reactserver'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('details/<int:project_id>', views.DetailsView.as_view(), name='details')
]
