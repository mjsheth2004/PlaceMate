from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, date, time

from apps.accounts.models import User
from .models import CompanyProfile
from .forms import CompanyProfileForm, PlacementDriveForm
from apps.common.models import PlacementDrive, Department, Skill
from apps.student_portal.models import Application, StudentProfile, InterviewSchedule

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
    
    applications = Application.objects.filter(drive__company=company_profile).select_related('student', 'student__department', 'drive')
    total_applications_count = applications.count()
    applied_count = applications.filter(status='applied').count()
    shortlisted_count = applications.filter(status='shortlisted').count()
    interview_scheduled_count = applications.filter(status='interview_scheduled').count()
    selected_count = applications.filter(status='selected').count()
    rejected_count = applications.filter(status='rejected').count()

    # Active scheduled interviews for this company
    raw_interviews = list(InterviewSchedule.objects.filter(
        application__drive__company=company_profile,
        status='scheduled'
    ).select_related(
        'application',
        'application__student',
        'application__student__department',
        'application__student__user',
        'application__drive'
    ).order_by('interview_date', 'interview_time'))

    seen_apps = set()
    scheduled_interviews = []
    for itw in raw_interviews:
        if itw.application_id not in seen_apps:
            seen_apps.add(itw.application_id)
            scheduled_interviews.append(itw)

    interviews_scheduled_count = len(scheduled_interviews)
    reschedule_requested_count = sum(1 for itw in scheduled_interviews if itw.reschedule_requested)

    recent_applications = applications.order_by('-applied_at')[:6]
    recent_drives = PlacementDrive.objects.filter(
        company=company_profile
    ).annotate(
        applicant_count=Count('application')
    ).order_by('-created_at')[:5]

    context = {
        'company_profile': company_profile,
        'total_drives_count': total_drives_count,
        'published_drives_count': published_drives_count,
        'total_applications_count': total_applications_count,
        'applied_count': applied_count,
        'shortlisted_count': shortlisted_count,
        'interview_scheduled_count': interview_scheduled_count,
        'selected_count': selected_count,
        'rejected_count': rejected_count,
        'scheduled_interviews': scheduled_interviews,
        'interviews_scheduled_count': interviews_scheduled_count,
        'reschedule_requested_count': reschedule_requested_count,
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
    active_drives_count = PlacementDrive.objects.filter(company=company_profile, status='published').count()
    applications_count = Application.objects.filter(drive__company=company_profile).count()
    
    context = {
        'company_profile': company_profile,
        'drives_count': drives_count,
        'active_drives_count': active_drives_count,
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
    applications = Application.objects.filter(drive=drive).select_related(
        'student', 'student__department', 'student__user'
    ).prefetch_related('interview_schedules').order_by('-applied_at')
    
    if status_filter and status_filter != 'all':
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
    ).prefetch_related('interview_schedules').order_by('-applied_at')
    
    if selected_drive_id and selected_drive_id.isdigit():
        applications = applications.filter(drive_id=int(selected_drive_id))
        
    if status_filter and status_filter != 'all':
        applications = applications.filter(status=status_filter)
        
    if search_query:
        applications = applications.filter(
            Q(student__full_name__icontains=search_query) |
            Q(student__roll_number__icontains=search_query) |
            Q(student__user__email__icontains=search_query) |
            Q(drive__title__icontains=search_query)
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
            application.status = new_status
            application.save() # Handled by student_portal signals.py to prevent duplicate emails
            messages.success(request, f"Application status updated for {application.student.full_name} to '{application.get_status_display()}'.")
        else:
            messages.error(request, "Invalid status choice.")
            
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or redirect('company_portal:applicants_list').url
    return redirect(next_url)


@company_required
def schedule_interview_view(request):
    if request.method != 'POST':
        return redirect('company_portal:applicants_list')
        
    company_profile, created = CompanyProfile.objects.get_or_create(user=request.user)
    application_id = request.POST.get('application_id')
    application = get_object_or_404(Application, pk=application_id, drive__company=company_profile)
    
    interview_date = request.POST.get('interview_date')
    interview_time = request.POST.get('interview_time')
    interview_mode = request.POST.get('interview_mode', 'online')
    location_address = request.POST.get('location_address', '').strip()
    meeting_link = request.POST.get('meeting_link', '').strip()
    description = request.POST.get('description', '').strip()
    
    if not interview_date or not interview_time:
        messages.error(request, "Please specify both interview date and time.")
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or redirect('company_portal:applicants_list').url
        return redirect(next_url)
        
    # Store or update interview schedule in database (delete any old meetings for this application so only 1 exists)
    InterviewSchedule.objects.filter(application=application).delete()
    interview = InterviewSchedule.objects.create(
        application=application,
        interview_date=interview_date,
        interview_time=interview_time,
        interview_mode=interview_mode,
        location_address=location_address,
        meeting_link=meeting_link,
        description=description,
        status='scheduled',
        reschedule_requested=False,
        reschedule_reason=''
    )
    
    # Update application status to interview_scheduled (suppress generic status email, since detailed invitation email is sent below)
    application.status = 'interview_scheduled'
    application._skip_status_email = True
    application.save()

    
    # Refresh to ensure DB model types
    interview.refresh_from_db()

    # Format human-readable date and time strings directly for guaranteed email rendering
    try:
        if isinstance(interview.interview_date, (datetime, date)):
            formatted_date = interview.interview_date.strftime('%A, %B %d, %Y')
        else:
            formatted_date = datetime.strptime(str(interview.interview_date), '%Y-%m-%d').strftime('%A, %B %d, %Y')
    except Exception:
        formatted_date = str(interview.interview_date)

    try:
        if isinstance(interview.interview_time, (datetime, time)):
            formatted_time = interview.interview_time.strftime('%I:%M %p')
        else:
            time_str = str(interview.interview_time).split('.')[0]
            if len(time_str.split(':')) == 3:
                formatted_time = datetime.strptime(time_str, '%H:%M:%S').strftime('%I:%M %p')
            else:
                formatted_time = datetime.strptime(time_str, '%H:%M').strftime('%I:%M %p')
    except Exception:
        formatted_time = str(interview.interview_time)

    # Send interview invitation email to student candidate
    email_sent = False
    try:
        html_message = render_to_string('emails/interview_schedule_notification.html', {
            'student_name': application.student.full_name,
            'company_name': company_profile.company_name,
            'drive_title': application.drive.title,
            'interview': interview,
            'formatted_date': formatted_date,
            'formatted_time': formatted_time,
        })
        
        mode_text = "Online" if interview_mode == "online" else "In-Person (Offline)"
        plain_message = (
            f"Dear {application.student.full_name},\n\n"
            f"An interview has been scheduled for your application to {application.drive.title} at {company_profile.company_name}.\n\n"
            f"Date: {formatted_date}\n"
            f"Time: {formatted_time}\n"
            f"Mode: {mode_text}\n"
        )
        if interview_mode == 'offline':
            plain_message += f"Venue / Address: {location_address}\n"
        else:
            if meeting_link:
                plain_message += f"Meeting Link: {meeting_link}\n"
        if description:
            plain_message += f"\nDescription / Instructions: {description}\n"
        plain_message += f"\nBest regards,\n{company_profile.company_name}"
        
        send_mail(
            subject=f"Interview Scheduled: {application.drive.title} at {company_profile.company_name}",
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[application.student.user.email],
            html_message=html_message,
            fail_silently=False
        )
        email_sent = True
    except Exception as e:
        print(f"Error sending interview schedule email: {e}")
        email_sent = False
        
    if email_sent:
        messages.success(request, f"Interview scheduled for {application.student.full_name} and invitation email sent to {application.student.user.email}!")
    else:
        messages.success(request, f"Interview scheduled for {application.student.full_name} and recorded in database.")
        
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or redirect('company_portal:applicants_list').url
    return redirect(next_url)



import json
from django.db.models import Avg

@company_required
def analytics_view(request):
    company_profile, created = CompanyProfile.objects.get_or_create(
        user=request.user,
        defaults={'company_name': request.user.first_name or request.user.email}
    )
    
    drives = PlacementDrive.objects.filter(company=company_profile)
    total_drives_count = drives.count()
    published_drives_count = drives.filter(status='published').count()
    
    applications = Application.objects.filter(drive__company=company_profile).select_related('student', 'student__department', 'student__user', 'drive')
    total_applicants_count = applications.count()
    
    applied_count = applications.filter(status='applied').count()
    shortlisted_count = applications.filter(status='shortlisted').count()
    interview_count = applications.filter(status='interview_scheduled').count()
    selected_count = applications.filter(status='selected').count()
    rejected_count = applications.filter(status='rejected').count()
    
    shortlist_rate = round(((shortlisted_count + interview_count + selected_count) / total_applicants_count * 100), 1) if total_applicants_count > 0 else 0
    selection_rate = round((selected_count / total_applicants_count * 100), 1) if total_applicants_count > 0 else 0
    
    avg_cgpa_val = applications.aggregate(Avg('student__cgpa'))['student__cgpa__avg']
    avg_cgpa = round(avg_cgpa_val, 2) if avg_cgpa_val is not None else 0.0
    
    avg_applicants_per_drive = round(total_applicants_count / total_drives_count, 1) if total_drives_count > 0 else 0

    # 1. Funnel Chart JSON
    funnel_chart_json = json.dumps({
        'labels': ['Applied', 'Shortlisted', 'Interview Scheduled', 'Selected (Hired)', 'Rejected'],
        'data': [applied_count, shortlisted_count, interview_count, selected_count, rejected_count]
    })

    # 2. Drive Comparison Chart (Applicants vs Hires per drive)
    drive_labels = []
    drive_applicants = []
    drive_hires = []
    for d in drives.order_by('-created_at')[:6]:
        drive_labels.append(d.title[:18] + ('...' if len(d.title) > 18 else ''))
        drive_applicants.append(d.application_set.count())
        drive_hires.append(d.application_set.filter(status='selected').count())
        
    drive_comparison_json = json.dumps({
        'labels': drive_labels,
        'applicants': drive_applicants,
        'hires': drive_hires
    })

    # 3. Department Split Chart
    dept_map = {}
    for app in applications:
        dept_name = app.student.department.name if app.student.department else 'Other'
        dept_map[dept_name] = dept_map.get(dept_name, 0) + 1
        
    dept_chart_json = json.dumps({
        'labels': list(dept_map.keys()) if dept_map else ['No Applicants'],
        'data': list(dept_map.values()) if dept_map else [0]
    })

    # 4. Candidate CGPA Spread
    cgpa_bins = {'< 6.0': 0, '6.0 - 7.0': 0, '7.0 - 8.0': 0, '8.0 - 9.0': 0, '9.0 - 10.0': 0}
    for app in applications:
        try:
            cgpa_val = float(app.student.cgpa or 0)
            if cgpa_val < 6.0:
                cgpa_bins['< 6.0'] += 1
            elif cgpa_val < 7.0:
                cgpa_bins['6.0 - 7.0'] += 1
            elif cgpa_val < 8.0:
                cgpa_bins['7.0 - 8.0'] += 1
            elif cgpa_val < 9.0:
                cgpa_bins['8.0 - 9.0'] += 1
            else:
                cgpa_bins['9.0 - 10.0'] += 1
        except (ValueError, TypeError):
            cgpa_bins['< 6.0'] += 1

    cgpa_chart_json = json.dumps({
        'labels': list(cgpa_bins.keys()),
        'data': list(cgpa_bins.values())
    })

    # Detailed Drive Performance Breakdown Table
    drives_summary = []
    for d in drives.order_by('-created_at'):
        d_apps = d.application_set.all()
        d_total = d_apps.count()
        d_short = d_apps.filter(status='shortlisted').count()
        d_selected = d_apps.filter(status='selected').count()
        d_avg_cgpa = d_apps.aggregate(Avg('student__cgpa'))['student__cgpa__avg']
        d_hire_rate = round(d_selected / d_total * 100, 1) if d_total > 0 else 0
        
        drives_summary.append({
            'drive': d,
            'total_applicants': d_total,
            'shortlisted_count': d_short,
            'selected_count': d_selected,
            'avg_cgpa': round(d_avg_cgpa, 2) if d_avg_cgpa is not None else 'N/A',
            'hire_rate': d_hire_rate
        })

    context = {
        'company_profile': company_profile,
        'published_drives_count': published_drives_count,
        'total_applicants_count': total_applicants_count,
        'shortlisted_count': shortlisted_count,
        'selected_count': selected_count,
        'shortlist_rate': shortlist_rate,
        'selection_rate': selection_rate,
        'avg_cgpa': avg_cgpa,
        'avg_applicants_per_drive': avg_applicants_per_drive,
        'funnel_chart_json': funnel_chart_json,
        'drive_comparison_json': drive_comparison_json,
        'dept_chart_json': dept_chart_json,
        'cgpa_chart_json': cgpa_chart_json,
        'drives_summary': drives_summary,
    }
    return render(request, 'company_portal/analytics.html', context)

