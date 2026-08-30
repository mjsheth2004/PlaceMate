from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Application
from apps.common.models import PlacementDrive

@login_required
def dashboard_view(request):
    try:
        profile = request.user.studentprofile
    except:
        return render(request, 'student_portal/dashboard.html', {'error': 'Profile not found.'})

    # Calculate profile completeness
    fields_to_check = ['resume', 'profile_photo', 'cgpa', 'passing_year', 'skills']
    filled_fields = 0
    for field in fields_to_check:
        val = getattr(profile, field, None)
        # For ManyToMany skills
        if field == 'skills':
            if val.exists():
                filled_fields += 1
        elif val:
            filled_fields += 1
            
    completion_percentage = int((filled_fields / len(fields_to_check)) * 100)

    applications = Application.objects.filter(student=profile).select_related('drive', 'drive__company').order_by('-applied_at')[:5]

    now = timezone.now()
    applied_drive_ids = Application.objects.filter(student=profile).values_list('drive_id', flat=True)
    
    # Base eligible filter
    eligible_drives = PlacementDrive.objects.filter(
        status='published',
        application_deadline__gt=now,
        eligible_departments=profile.department_id,
        min_cgpa__lte=profile.cgpa or 0.0,
        max_backlogs__gte=profile.active_backlogs or 0,
        eligible_passing_year=profile.passing_year or 0
    ).exclude(id__in=applied_drive_ids).select_related('company').order_by('application_deadline')[:5]

    # KPI Stats
    total_applications = Application.objects.filter(student=profile).count()
    interviews_scheduled = Application.objects.filter(student=profile, status='interview_scheduled').count()
    offers_received = Application.objects.filter(student=profile, status='selected').count()
    total_eligible_drives = PlacementDrive.objects.filter(
        status='published',
        application_deadline__gt=now,
        eligible_departments=profile.department_id,
        min_cgpa__lte=profile.cgpa or 0.0,
        max_backlogs__gte=profile.active_backlogs or 0,
        eligible_passing_year=profile.passing_year or 0
    ).exclude(id__in=applied_drive_ids).count()

    context = {
        'completion_percentage': completion_percentage,
        'applications': applications,
        'eligible_drives': eligible_drives,
        'total_applications': total_applications,
        'interviews_scheduled': interviews_scheduled,
        'offers_received': offers_received,
        'total_eligible_drives': total_eligible_drives,
    }
    return render(request, 'student_portal/dashboard.html', context)

from django.shortcuts import redirect
from django.contrib import messages
from .models import StudentProfile
from .forms import StudentProfileForm

@login_required
def profile_view(request):
    profile = request.user.studentprofile
    return render(request, 'student_portal/profile.html', {'profile': profile})

@login_required
def edit_profile_view(request):
    profile = request.user.studentprofile
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('student_portal:profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = StudentProfileForm(instance=profile)
    
    return render(request, 'student_portal/edit_profile.html', {'form': form})

from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

@login_required
def drives_list_view(request):
    profile = request.user.studentprofile
    now = timezone.now()
    
    # All active published drives
    all_drives = PlacementDrive.objects.filter(
        status='published',
        application_deadline__gt=now
    ).select_related('company').order_by('application_deadline')
    
    # Get IDs of drives student has applied to
    applied_drive_ids = Application.objects.filter(student=profile).values_list('drive_id', flat=True)
    
    # Prepare list with eligibility data
    drives_data = []
    for drive in all_drives:
        is_eligible = True
        reasons = []
        
        # Check eligibility
        if profile.department not in drive.eligible_departments.all():
            is_eligible = False
            reasons.append("Department not eligible")
        if (profile.cgpa or 0.0) < drive.min_cgpa:
            is_eligible = False
            reasons.append(f"CGPA below {drive.min_cgpa}")
        if (profile.active_backlogs or 0) > drive.max_backlogs:
            is_eligible = False
            reasons.append("Active backlogs exceed limit")
        if profile.passing_year != drive.eligible_passing_year:
            is_eligible = False
            reasons.append(f"Passing year must be {drive.eligible_passing_year}")
            
        has_applied = drive.id in applied_drive_ids
        
        drives_data.append({
            'drive': drive,
            'is_eligible': is_eligible,
            'reasons': reasons,
            'has_applied': has_applied
        })
        
    return render(request, 'student_portal/drives_list.html', {
        'drives_data': drives_data
    })

@login_required
def drive_detail_view(request, drive_id):
    profile = request.user.studentprofile
    drive = get_object_or_404(PlacementDrive.objects.select_related('company').prefetch_related('required_skills', 'eligible_departments'), id=drive_id, status='published')
    
    has_applied = Application.objects.filter(student=profile, drive=drive).exists()
    
    # Check eligibility
    is_eligible = True
    reasons = []
    if profile.department not in drive.eligible_departments.all():
        is_eligible = False
        reasons.append("Department not eligible")
    if (profile.cgpa or 0.0) < drive.min_cgpa:
        is_eligible = False
        reasons.append(f"CGPA below {drive.min_cgpa}")
    if (profile.active_backlogs or 0) > drive.max_backlogs:
        is_eligible = False
        reasons.append("Active backlogs exceed limit")
    if profile.passing_year != drive.eligible_passing_year:
        is_eligible = False
        reasons.append(f"Passing year must be {drive.eligible_passing_year}")
    
    # Check if profile is complete (for allowing application)
    fields_to_check = ['resume', 'profile_photo', 'cgpa', 'passing_year', 'skills']
    profile_complete = True
    for field in fields_to_check:
        val = getattr(profile, field, None)
        if field == 'skills':
            if not val.exists():
                profile_complete = False
        elif not val:
            profile_complete = False

    return render(request, 'student_portal/drive_detail.html', {
        'drive': drive,
        'has_applied': has_applied,
        'is_eligible': is_eligible,
        'eligibility_reasons': reasons,
        'profile_complete': profile_complete,
        'is_expired': drive.application_deadline < timezone.now()
    })

@login_required
def apply_for_drive_view(request, drive_id):
    if request.method != 'POST':
        return redirect('student_portal:drive_detail', drive_id=drive_id)
        
    profile = request.user.studentprofile
    drive = get_object_or_404(PlacementDrive, id=drive_id, status='published')
    
    if drive.application_deadline < timezone.now():
        messages.error(request, "Application deadline has passed.")
        return redirect('student_portal:drive_detail', drive_id=drive_id)
        
    if Application.objects.filter(student=profile, drive=drive).exists():
        messages.info(request, "You have already applied to this drive.")
        return redirect('student_portal:drive_detail', drive_id=drive_id)
        
    # Verify eligibility again on backend
    if profile.department not in drive.eligible_departments.all() or \
       (profile.cgpa or 0.0) < drive.min_cgpa or \
       (profile.active_backlogs or 0) > drive.max_backlogs or \
       profile.passing_year != drive.eligible_passing_year:
        messages.error(request, "You do not meet the eligibility criteria for this drive.")
        return redirect('student_portal:drive_detail', drive_id=drive_id)
        
    # Create application
    Application.objects.create(student=profile, drive=drive, status='applied')
    messages.success(request, f"Successfully applied to {drive.company.company_name} - {drive.title}")
    
    # Send Confirmation Email
    subject = f"Application Received: {drive.company.company_name} - {drive.title}"
    message = f"""Hi {profile.full_name or request.user.username},

You have successfully applied for the {drive.title} role at {drive.company.company_name}.

Drive Details:
- Role: {drive.title}
- Company: {drive.company.company_name}
- Location: {drive.location}
- Package: {drive.salary_package}

Description:
{drive.job_description}

You can track the status of your application in the "My Applications" section of your PlaceMate portal.

Best of luck!
The PlaceMate Team
"""
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Failed to send email: {e}")
    
    return redirect('student_portal:drive_detail', drive_id=drive_id)

@login_required
def applications_list_view(request):
    profile = request.user.studentprofile
    
    applications = Application.objects.filter(student=profile).select_related(
        'drive', 'drive__company'
    ).order_by('-applied_at')
    
    return render(request, 'student_portal/applications_list.html', {
        'applications': applications
    })

import json
from datetime import datetime
from django.db.models import Count, Q
from apps.common.models import Skill

@login_required
def analytics_view(request):
    try:
        profile = request.user.studentprofile
    except Exception:
        return redirect('student_portal:profile')

    now = timezone.now()
    applications = Application.objects.filter(student=profile).select_related('drive', 'drive__company')
    total_applications = applications.count()
    
    applied_count = applications.filter(status='applied').count()
    shortlisted_count = applications.filter(status='shortlisted').count()
    interview_count = applications.filter(status='interview_scheduled').count()
    selected_count = applications.filter(status='selected').count()
    rejected_count = applications.filter(status='rejected').count()

    shortlist_rate = round(((shortlisted_count + interview_count + selected_count) / total_applications * 100), 1) if total_applications > 0 else 0
    offer_rate = round((selected_count / total_applications * 100), 1) if total_applications > 0 else 0

    # 1. Status Chart JSON
    status_chart_json = json.dumps({
        'labels': ['Applied', 'Shortlisted', 'Interview Scheduled', 'Selected', 'Rejected'],
        'data': [applied_count, shortlisted_count, interview_count, selected_count, rejected_count]
    })

    # 2. Salary Tier Distribution of applied drives
    salary_tiers = {'< 6 LPA': 0, '6 - 10 LPA': 0, '10 - 15 LPA': 0, '15+ LPA': 0}
    for app in applications:
        try:
            pkg = float(app.drive.salary_package)
            if pkg < 6.0:
                salary_tiers['< 6 LPA'] += 1
            elif pkg <= 10.0:
                salary_tiers['6 - 10 LPA'] += 1
            elif pkg <= 15.0:
                salary_tiers['10 - 15 LPA'] += 1
            else:
                salary_tiers['15+ LPA'] += 1
        except (ValueError, TypeError):
            salary_tiers['< 6 LPA'] += 1

    salary_tier_json = json.dumps({
        'labels': list(salary_tiers.keys()),
        'data': list(salary_tiers.values())
    })

    # 3. Application Activity Timeline (last 6 months)
    month_labels = []
    month_counts = []
    for i in range(5, -1, -1):
        year = now.year
        month = now.month - i
        while month <= 0:
            month += 12
            year -= 1
        m_name = datetime(year, month, 1).strftime('%b %Y')
        month_labels.append(m_name)
        m_count = applications.filter(applied_at__year=year, applied_at__month=month).count()
        month_counts.append(m_count)

    timeline_json = json.dumps({
        'labels': month_labels,
        'data': month_counts
    })

    # 4. Skill Demand Alignment
    student_skills = profile.skills.all()
    skill_labels = []
    skill_data = []
    if student_skills.exists():
        for sk in student_skills[:8]:
            d_count = PlacementDrive.objects.filter(status='published', required_skills=sk).count()
            skill_labels.append(sk.name)
            skill_data.append(d_count)
    else:
        top_skills = Skill.objects.annotate(drive_count=Count('placementdrive', filter=Q(placementdrive__status='published'))).order_by('-drive_count')[:6]
        for sk in top_skills:
            skill_labels.append(sk.name)
            skill_data.append(sk.drive_count)

    skill_data_json = json.dumps({
        'labels': skill_labels,
        'data': skill_data
    })

    recent_applications = applications.order_by('-applied_at')[:8]
    applied_drive_ids = applications.values_list('drive_id', flat=True)
    recommended_drives = PlacementDrive.objects.filter(
        status='published',
        application_deadline__gt=now,
        eligible_departments=profile.department_id,
        min_cgpa__lte=profile.cgpa or 0.0,
        max_backlogs__gte=profile.active_backlogs or 0,
        eligible_passing_year=profile.passing_year or 0
    ).exclude(id__in=applied_drive_ids).select_related('company').order_by('application_deadline')[:5]

    context = {
        'total_applications': total_applications,
        'shortlisted_count': shortlisted_count,
        'shortlist_rate': shortlist_rate,
        'interview_count': interview_count,
        'selected_count': selected_count,
        'offer_rate': offer_rate,
        'status_chart_json': status_chart_json,
        'salary_tier_json': salary_tier_json,
        'timeline_json': timeline_json,
        'skill_data_json': skill_data_json,
        'recent_applications': recent_applications,
        'recommended_drives': recommended_drives,
    }
    return render(request, 'student_portal/analytics.html', context)

