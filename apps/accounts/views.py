import random
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import StudentRegistrationForm, CompanyRegistrationForm
from .models import User, EmailOTP
from apps.student_portal.models import StudentProfile
from apps.company_portal.models import CompanyProfile
from apps.common.models import Department

@login_required
def login_redirect_view(request):
    user = request.user
    if user.is_superuser or user.role == User.OFFICER:
        return redirect('/admin/')
    elif user.role == User.STUDENT:
        return redirect('student_portal:dashboard')
    elif user.role == User.COMPANY:
        return redirect('company_portal:dashboard')
    else:
        return redirect('accounts:login')


def register_selection_view(request):
    return render(request, 'accounts/register_selection.html')

def presentation_view(request):
    return render(request, 'presentation.html')

@require_POST
def send_registration_otp_view(request):
    email = request.POST.get('email', '').strip().lower()
    if not email:
        return JsonResponse({'success': False, 'message': 'Email address is required.'})
    
    if User.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'message': 'An account with this email is already registered.'})
    
    # Invalidate previous unverified OTPs for this email
    EmailOTP.objects.filter(email=email, is_verified=False).delete()
    
    # Generate 6-digit OTP
    otp = f"{random.randint(100000, 999999)}"
    EmailOTP.objects.create(email=email, otp=otp)
    
    # Send email
    subject = "PlaceMate - Email Verification Code"
    html_message = render_to_string('emails/otp_verification.html', {'otp': otp})
    plain_message = f"Your PlaceMate registration verification code is: {otp}\n\nThis code will expire in 10 minutes."
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False
        )
        return JsonResponse({'success': True, 'message': f'Verification code sent to {email}.'})
    except Exception as e:
        print(f"Error sending OTP to {email}: {e}")
        return JsonResponse({'success': False, 'message': 'Failed to send email. Please verify your email address.'})


@require_POST
def verify_registration_otp_view(request):
    email = request.POST.get('email', '').strip().lower()
    otp = request.POST.get('otp', '').strip()
    
    if not email or not otp:
        return JsonResponse({'success': False, 'message': 'Email and OTP are both required.'})
    
    otp_record = EmailOTP.objects.filter(email=email, is_verified=False).order_by('-created_at').first()
    
    if not otp_record:
        return JsonResponse({'success': False, 'message': 'No pending OTP verification found for this email. Please request an OTP.'})
    
    if not otp_record.is_valid():
        return JsonResponse({'success': False, 'message': 'OTP has expired (10 minute limit). Please request a new one.'})
    
    if otp_record.otp != otp:
        return JsonResponse({'success': False, 'message': 'Invalid verification code. Please check and try again.'})
    
    otp_record.is_verified = True
    otp_record.save()
    
    request.session['verified_registration_email'] = email
    
    return JsonResponse({'success': True, 'message': 'Email verified successfully!'})


def register_student_view(request):
    # Ensure default departments exist so the form doesn't fail
    if not Department.objects.exists():
        Department.objects.create(name="Computer Engineering", code="CE")
        Department.objects.create(name="Information Technology", code="IT")
        Department.objects.create(name="Mechanical Engineering", code="ME")
        
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        is_verified = EmailOTP.objects.filter(email=email, is_verified=True).exists() or (request.session.get('verified_registration_email') == email)
        
        if not is_verified:
            messages.error(request, "Please verify your email with the OTP before submitting registration.")
            departments = Department.objects.all()
            return render(request, 'accounts/register_student.html', {'departments': departments})

        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            name_parts = full_name.split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                role=User.STUDENT,
                first_name=first_name,
                last_name=last_name,
                email_verified=True
            )
            StudentProfile.objects.create(
                user=user,
                full_name=full_name,
                roll_number=form.cleaned_data['roll_number'],
                university=form.cleaned_data['university'],
                department=form.cleaned_data['department'],
                semester=form.cleaned_data['semester'],
                cgpa=form.cleaned_data['cgpa'],
                passing_year=form.cleaned_data['passing_year'],
                active_backlogs=form.cleaned_data['active_backlogs']
            )
            # Clear session
            request.session.pop('verified_registration_email', None)
            
            login(request, user)
            
            # Send Welcome Email
            try:
                login_url = request.build_absolute_uri('/accounts/')
                html_message = render_to_string('emails/welcome_student.html', {
                    'name': full_name,
                    'login_url': login_url
                })
                send_mail(
                    subject="Welcome to PlaceMate!",
                    message=f"Hi {full_name},\n\nWelcome to PlaceMate! Log in at {login_url} to explore placement drives.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=True
                )
            except Exception as e:
                print(f"Failed to send student welcome email: {e}")

            messages.success(request, "Student registration successful.")
            return redirect('student_portal:dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    departments = Department.objects.all()
    return render(request, 'accounts/register_student.html', {'departments': departments})

def register_company_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        is_verified = EmailOTP.objects.filter(email=email, is_verified=True).exists() or (request.session.get('verified_registration_email') == email)
        
        if not is_verified:
            messages.error(request, "Please verify your email with the OTP before submitting registration.")
            return render(request, 'accounts/register_company.html')

        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                role=User.COMPANY,
                first_name=company_name,
                email_verified=True
            )
            CompanyProfile.objects.create(
                user=user,
                company_name=company_name,
                industry=form.cleaned_data['industry'],
                website=form.cleaned_data['website'],
                location=form.cleaned_data['location'],
                description=form.cleaned_data['description']
            )
            # Clear session
            request.session.pop('verified_registration_email', None)
            
            login(request, user)

            # Send Welcome Email
            try:
                login_url = request.build_absolute_uri('/accounts/')
                html_message = render_to_string('emails/welcome_company.html', {
                    'company_name': company_name,
                    'login_url': login_url
                })
                send_mail(
                    subject="Welcome to PlaceMate Recruiter Portal!",
                    message=f"Hi {company_name},\n\nWelcome to PlaceMate! Log in at {login_url} to manage recruitment drives.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=True
                )
            except Exception as e:
                print(f"Failed to send company welcome email: {e}")

            messages.success(request, "Company registration successful.")
            return redirect('company_portal:dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    return render(request, 'accounts/register_company.html')


