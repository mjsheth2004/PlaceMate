from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('redirect/', views.login_redirect_view, name='login_redirect'),
    path('register/', views.register_selection_view, name='register'),
    path('register/student/', views.register_student_view, name='register_student'),
    path('register/company/', views.register_company_view, name='register_company'),
    path('forgot-password/', auth_views.PasswordResetView.as_view(template_name='accounts/forgot_password.html'), name='forgot_password'),
]
