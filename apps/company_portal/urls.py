from django.urls import path
from . import views

app_name = 'company_portal'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('drives/', views.drives_list_view, name='drives_list'),
    path('drives/create/', views.create_drive_view, name='create_drive'),
    path('drives/<int:pk>/', views.drive_detail_view, name='drive_detail'),
    path('drives/<int:pk>/edit/', views.edit_drive_view, name='edit_drive'),
    path('applicants/', views.applicants_list_view, name='applicants_list'),
    path('application/<int:pk>/status/', views.update_application_status_view, name='update_application_status'),
]
