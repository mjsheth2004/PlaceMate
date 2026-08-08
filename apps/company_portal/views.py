from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from apps.accounts.models import User
from .models import CompanyProfile
from .forms import CompanyProfileForm, PlacementDriveForm
from apps.common.models import PlacementDrive, Department, Skill
from apps.student_portal.models import Application, StudentProfile

def company_required(view_func):
    """Decorator to restrict access only to Company accounts."""
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role != User.COMPANY and not request.user.is_superuser:
            messages.error(request, "Access denied. Company portal only.")
            return redirect('accounts:login_redirect')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@company_required
def dashboard_view(request):
    company_profile, created = CompanyProfile.objects.get_or_create(
        user=request.user,
        defaults={'company_name': request.user.first_name or request.user.email}
    )
    
    drives = PlacementDrive.objects.filter(company=company_profile)
    total_drives_count = drives.count()
    published_drives_count = drives.filter(status='published').count()
    
    applications = Application.objects.filter(drive__company=company_profile).select_related('student', 'drive')
    total_applications_count = applications.count()
    shortlisted_count = applications.filter(status='shortlisted').count()
    selected_count = applications.filter(status='selected').count()
    
    recent_applications = applications.order_by('-applied_at')[:5]
    recent_drives = drives.order_by('-created_at')[:4]
    
    context = {
        'company_profile': company_profile,
        'total_drives_count': total_drives_count,
        'published_drives_count': published_drives_count,
        'total_applications_count': total_applications_count,
        'shortlisted_count': shortlisted_count,
        'selected_count': selected_count,
        'recent_applications': recent_applications,
        'recent_drives': recent_drives,
    }
    return render(request, 'company_portal/dashboard.html', context)


@company_required
def profile_view(request):
    company_profile, created = CompanyProfile.objects.get_or_create(
        user=request.user,
        defaults={'company_name': request.user.first_name or request.user.email}
    )
    drives_count = PlacementDrive.objects.filter(company=company_profile).count()
    applications_count = Application.objects.filter(drive__company=company_profile).count()
    
    context = {
        'company_profile': company_profile,
        'drives_count': drives_count,
        'applications_count': applications_count,
    }
    return render(request, 'company_portal/profile.html', context)


@company_required
def edit_profile_view(request):
    company_profile, created = CompanyProfile.objects.get_or_create(
        user=request.user,
        defaults={'company_name': request.user.first_name or request.user.email}
    )
    
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=company_profile)
        if form.is_valid():
            form.save()
            # Also update user first_name if changed
            request.user.first_name = company_profile.company_name
            request.user.save()
            messages.success(request, "Company profile updated successfully.")
            return redirect('company_portal:profile')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CompanyProfileForm(instance=company_profile)
        
    return render(request, 'company_portal/edit_profile.html', {'form': form, 'company_profile': company_profile})


@company_required
def drives_list_view(request):
    company_profile, created = CompanyProfile.objects.get_or_create(user=request.user)
    status_filter = request.GET.get('status', 'all')
    
    drives = PlacementDrive.objects.filter(company=company_profile).annotate(
        applicant_count=Count('application')
    ).order_by('-created_at')
    
    if status_filter in ['draft', 'published', 'closed']:
        drives = drives.filter(status=status_filter)
        
    context = {
        'drives': drives,
        'status_filter': status_filter,
    }
    return render(request, 'company_portal/drives_list.html', context)


@company_required
def create_drive_view(request):
    company_profile, created = CompanyProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = PlacementDriveForm(request.POST)
        if form.is_valid():
            drive = form.save(commit=False)
            drive.company = company_profile
            drive.save()
            form.save_m2m() # save departments and skills
            messages.success(request, f"Placement Drive '{drive.title}' created successfully.")
            return redirect('company_portal:drives_list')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = PlacementDriveForm()
        
    return render(request, 'company_portal/create_drive.html', {'form': form})


@company_required
def edit_drive_view(request, pk):
    company_profile, created = CompanyProfile.objects.get_or_create(user=request.user)
    drive = get_object_or_404(PlacementDrive, pk=pk, company=company_profile)
    
    if request.method == 'POST':
        form = PlacementDriveForm(request.POST, instance=drive)
        if form.is_valid():
            form.save()
            messages.success(request, f"Placement Drive '{drive.title}' updated successfully.")
            return redirect('company_portal:drive_detail', pk=drive.pk)
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = PlacementDriveForm(instance=drive)
        
    return render(request, 'company_portal/edit_drive.html', {'form': form, 'drive': drive})


@company_required
def drive_detail_view(request, pk):
    company_profile, created = CompanyProfile.objects.get_or_create(user=request.user)
    drive = get_object_or_404(PlacementDrive, pk=pk, company=company_profile)
    
    status_filter = request.GET.get('status', 'all')
    applications = Application.objects.filter(drive=drive).select_related('student', 'student__department', 'student__user').order_by('-applied_at')
    
    if status_filter != 'all':
        applications = applications.filter(status=status_filter)
        
    context = {
        'drive': drive,
        'applications': applications,
        'status_filter': status_filter,
        'total_applicants': drive.application_set.count(),
        'shortlisted_count': drive.application_set.filter(status='shortlisted').count(),
        'selected_count': drive.application_set.filter(status='selected').count(),
    }
    return render(request, 'company_portal/drive_detail.html', context)


@company_required
def applicants_list_view(request):
    company_profile, created = CompanyProfile.objects.get_or_create(user=request.user)
    
    drives = PlacementDrive.objects.filter(company=company_profile)
    selected_drive_id = request.GET.get('drive', '')
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('q', '').strip()
    
    applications = Application.objects.filter(drive__company=company_profile).select_related(
        'student', 'student__department', 'student__user', 'drive'
    ).order_by('-applied_at')
    
    if selected_drive_id and selected_drive_id.isdigit():
        applications = applications.filter(drive_id=int(selected_drive_id))
        
    if status_filter != 'all':
        applications = applications.filter(status=status_filter)
        
    if search_query:
        applications = applications.filter(
            Q(student__full_name__icontains=search_query) |
            Q(student__roll_number__icontains=search_query) |
            Q(student__user__email__icontains=search_query)
        )
        
    context = {
        'applications': applications,
        'drives': drives,
        'selected_drive_id': selected_drive_id,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    return render(request, 'company_portal/applicants_list.html', context)


@company_required
def update_application_status_view(request, pk):
    company_profile, created = CompanyProfile.objects.get_or_create(user=request.user)
    application = get_object_or_404(Application, pk=pk, drive__company=company_profile)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid_statuses = [choice[0] for choice in Application.STATUS_CHOICES]
        
        if new_status in valid_statuses:
            old_status = application.get_status_display()
            application.status = new_status
            application.save()
            
            # Trigger notification email to student
            try:
                status_class_map = {
                    'selected': 'selected',
                    'shortlisted': 'shortlisted',
                    'interview_scheduled': 'interview',
                    'rejected': 'rejected',
                }
                status_class = status_class_map.get(new_status, 'shortlisted')
                portal_url = request.build_absolute_uri('/student/applications/')
                
                html_message = render_to_string('emails/application_status_update.html', {
                    'student_name': application.student.full_name,
                    'company_name': company_profile.company_name,
                    'drive_title': application.drive.title,
                    'status_class': status_class,
                    'status_display': application.get_status_display(),
                    'portal_url': portal_url,
                })
                
                send_mail(
                    subject=f"Application Update: {application.drive.title} at {company_profile.company_name}",
                    message=f"Hi {application.student.full_name},\nYour application status for {application.drive.title} has been updated to: {application.get_status_display()}.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[application.student.user.email],
                    html_message=html_message,
                    fail_silently=True
                )
            except Exception as e:
                print(f"Error sending application status update email: {e}")
                
            messages.success(request, f"Application status updated for {application.student.full_name} to '{application.get_status_display()}'.")
        else:
            messages.error(request, "Invalid status choice.")
            
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or redirect('company_portal:applicants_list').url
    return redirect(next_url)
