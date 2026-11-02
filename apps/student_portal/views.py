from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from .models import Application, InterviewSchedule, StudentProfile
from apps.common.models import PlacementDrive

@login_required
def dashboard_view(request):
    try:
        profile = request.user.studentprofile
    except Exception:
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

    applications = Application.objects.filter(student=profile).select_related(
        'drive', 'drive__company'
    ).prefetch_related('interview_schedules').order_by('-applied_at')[:5]

    # Fetch active scheduled interviews for this student, deduplicated by application
    raw_interviews = list(InterviewSchedule.objects.filter(
        application__student=profile,
        status='scheduled'
    ).select_related('application', 'application__drive', 'application__drive__company').order_by('interview_date', 'interview_time'))

    seen_apps = set()
    scheduled_interviews = []
    for itw in raw_interviews:
        if itw.application_id not in seen_apps:
            seen_apps.add(itw.application_id)
            scheduled_interviews.append(itw)

    # Detect clashes: check if any two interviews occur on the same date with overlapping time (within 60 mins)
    clash_detected = False
    for i in range(len(scheduled_interviews)):
        for j in range(i + 1, len(scheduled_interviews)):
            itw1 = scheduled_interviews[i]
            itw2 = scheduled_interviews[j]
            if itw1.interview_date == itw2.interview_date:
                t1 = itw1.interview_time
                t2 = itw2.interview_time
                mins1 = t1.hour * 60 + t1.minute
                mins2 = t2.hour * 60 + t2.minute
                if abs(mins1 - mins2) < 60:
                    itw1.has_clash = True
                    itw2.has_clash = True
                    clash_detected = True

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

    # Detailed Application Pipeline Stats for Hub Widget
    applied_only_count = Application.objects.filter(student=profile, status='applied').count()
    shortlisted_count = Application.objects.filter(student=profile, status='shortlisted').count()
    next_interview = scheduled_interviews[0] if scheduled_interviews else None
    days_until_interview = None
    if next_interview and next_interview.interview_date:
        days_until_interview = (next_interview.interview_date - now.date()).days

    context = {
        'profile': profile,
        'completion_percentage': completion_percentage,
        'applications': applications,
        'scheduled_interviews': scheduled_interviews,
        'clash_detected': clash_detected,
        'eligible_drives': eligible_drives,
        'total_applications': total_applications,
        'interviews_scheduled': interviews_scheduled,
        'offers_received': offers_received,
        'total_eligible_drives': total_eligible_drives,
        'applied_only_count': applied_only_count,
        'shortlisted_count': shortlisted_count,
        'next_interview': next_interview,
        'days_until_interview': days_until_interview,
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
    student_name = profile.full_name or request.user.username or request.user.email
    applications_url = request.build_absolute_uri(reverse('student_portal:applications_list'))

    html_message = render_to_string('emails/application_confirmation.html', {
        'student_name': student_name,
        'drive': drive,
        'applications_url': applications_url,
    })

    message = f"""Hi {student_name},

You have successfully applied for the {drive.title} role at {drive.company.company_name}.

Drive Details:
- Role: {drive.title}
- Company: {drive.company.company_name}
- Location: {drive.location}
- Package: ₹{drive.salary_package} LPA

You can track the status of your application in the "My Applications" section of your PlaceMate portal:
{applications_url}

Best of luck!
The PlaceMate Team
"""
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            html_message=html_message,
            fail_silently=True,
        )
    except Exception as e:
        print(f"Failed to send email: {e}")
    
    return redirect('student_portal:drive_detail', drive_id=drive_id)

@login_required
def applications_list_view(request):
    profile = request.user.studentprofile
    
    applications = list(Application.objects.filter(student=profile).select_related(
        'drive', 'drive__company'
    ).prefetch_related('interview_schedules').order_by('-applied_at'))
    
    # Collect scheduled interviews to detect time clashes
    scheduled_interviews = []
    for app in applications:
        for itw in app.interview_schedules.all():
            if itw.status == 'scheduled':
                scheduled_interviews.append(itw)
                
    clash_detected = False
    for i in range(len(scheduled_interviews)):
        for j in range(i + 1, len(scheduled_interviews)):
            itw1 = scheduled_interviews[i]
            itw2 = scheduled_interviews[j]
            if itw1.interview_date == itw2.interview_date:
                t1 = itw1.interview_time
                t2 = itw2.interview_time
                mins1 = t1.hour * 60 + t1.minute
                mins2 = t2.hour * 60 + t2.minute
                if abs(mins1 - mins2) < 60:
                    itw1.has_clash = True
                    itw2.has_clash = True
                    clash_detected = True

    return render(request, 'student_portal/applications_list.html', {
        'applications': applications,
        'clash_detected': clash_detected,
    })

@login_required
@require_POST
def request_interview_reschedule_view(request, interview_id):
    try:
        profile = request.user.studentprofile
    except Exception:
        messages.error(request, "Student profile required.")
        return redirect('student_portal:dashboard')

    interview = get_object_or_404(InterviewSchedule, pk=interview_id, application__student=profile)
    
    reason_category = request.POST.get('reason_category', 'clash').strip()
    reason_details = request.POST.get('reason_details', '').strip()
    suggested_time = request.POST.get('suggested_time', '').strip()
    
    category_labels = {
        'clash': 'Time Clash with Another Interview',
        'exam': 'College Exam / Academic Clash',
        'health': 'Medical Emergency / Health',
        'other': 'Scheduling Conflict'
    }
    category_display = category_labels.get(reason_category, 'Scheduling Conflict')
    
    parts = [f"[{category_display}]"]
    if reason_details:
        parts.append(reason_details)
    if suggested_time:
        parts.append(f"Candidate preferred slot: {suggested_time}")
        
    full_reason = " — ".join(parts)
        
    interview.reschedule_requested = True
    interview.reschedule_reason = full_reason
    interview.reschedule_requested_at = timezone.now()
    interview.save()
    
    # Notify recruiter via email
    company_email = interview.application.drive.company.user.email
    company_name = interview.application.drive.company.company_name
    drive_title = interview.application.drive.title
    student_name = profile.full_name or request.user.username
    
    try:
        subject = f"Interview Reschedule Request: {student_name} - {drive_title}"
        plain_message = f"""Dear {company_name} Recruitment Team,

Candidate {student_name} (Roll No: {profile.roll_number}) has requested to reschedule their interview for {drive_title}.

Current Schedule:
- Date: {interview.interview_date}
- Time: {interview.interview_time}
- Mode: {interview.get_interview_mode_display()}

Reason for Reschedule Request:
{full_reason}

You can reschedule their interview at:
{request.build_absolute_uri('/company/applicants/')}

Best regards,
PlaceMate Campus Placement System
"""
        html_message = render_to_string('emails/reschedule_request_notification.html', {
            'company_name': company_name,
            'student_name': student_name,
            'roll_number': profile.roll_number,
            'drive_title': drive_title,
            'interview': interview,
            'reason': full_reason,
            'portal_url': request.build_absolute_uri('/company/applicants/'),
        })
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[company_email],
            html_message=html_message,
            fail_silently=True,
        )
    except Exception as e:
        print(f"Error sending reschedule request email to company: {e}")
        
    messages.success(request, f"Reschedule request sent to {company_name}. They have been notified to review and update your interview time.")
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or redirect('student_portal:dashboard').url
    return redirect(next_url)

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

