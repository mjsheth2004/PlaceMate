from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .forms import StudentRegistrationForm, CompanyRegistrationForm
from .models import User
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

def register_student_view(request):
    # Ensure default departments exist so the form doesn't fail
    if not Department.objects.exists():
        Department.objects.create(name="Computer Engineering", code="CE")
        Department.objects.create(name="Information Technology", code="IT")
        Department.objects.create(name="Mechanical Engineering", code="ME")
        
    if request.method == 'POST':
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
                last_name=last_name
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
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                role=User.COMPANY,
                first_name=company_name
            )
            CompanyProfile.objects.create(
                user=user,
                company_name=company_name,
                industry=form.cleaned_data['industry'],
                website=form.cleaned_data['website'],
                location=form.cleaned_data['location'],
                description=form.cleaned_data['description']
            )
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

