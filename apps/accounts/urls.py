from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('redirect/', views.login_redirect_view, name='login_redirect'),
    path('register/', views.register_selection_view, name='register'),
    path('presentation/', views.presentation_view, name='presentation'),
    path('register/student/', views.register_student_view, name='register_student'),
    path('register/company/', views.register_company_view, name='register_company'),
    path('send-otp/', views.send_registration_otp_view, name='send_otp'),
    path('verify-otp/', views.verify_registration_otp_view, name='verify_otp'),
    path('forgot-password/', auth_views.PasswordResetView.as_view(
        template_name='accounts/forgot_password.html',
        email_template_name='registration/password_reset_email.html',
        html_email_template_name='emails/password_reset.html',
        subject_template_name='registration/password_reset_subject.txt',
        success_url=reverse_lazy('accounts:password_reset_done')
    ), name='forgot_password'),
    path('forgot-password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete')
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]
