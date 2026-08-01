from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_selection_view, name='register'),
    path('register/student/', views.register_student_view, name='register_student'),
    path('register/company/', views.register_company_view, name='register_company'),
]
