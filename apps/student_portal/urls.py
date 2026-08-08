from django.urls import path
from . import views

app_name = 'student_portal'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    
    # Placement Drives
    path('drives/', views.drives_list_view, name='drives_list'),
    path('drives/<int:drive_id>/', views.drive_detail_view, name='drive_detail'),
    path('drives/<int:drive_id>/apply/', views.apply_for_drive_view, name='apply_for_drive'),
    
    # Applications
    path('applications/', views.applications_list_view, name='applications_list'),
]
