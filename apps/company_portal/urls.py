from django.urls import path
from . import views

app_name = 'company_portal'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
]
