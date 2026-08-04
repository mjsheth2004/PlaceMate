from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, CompanyRegistrationForm
from .models import User
from apps.student_portal.models import StudentProfile
from apps.company_portal.models import CompanyProfile

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
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                role=User.STUDENT
            )
            StudentProfile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                roll_number=form.cleaned_data['roll_number'],
                university=form.cleaned_data['university'],
                department=form.cleaned_data['department'],
                semester=form.cleaned_data['semester'],
                cgpa=form.cleaned_data['cgpa'],
                passing_year=form.cleaned_data['passing_year'],
                active_backlogs=form.cleaned_data['active_backlogs']
            )
            login(request, user)
            messages.success(request, "Student registration successful.")
            return redirect('student_portal:dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    return render(request, 'accounts/register_student.html')

def register_company_view(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                role=User.COMPANY
            )
            CompanyProfile.objects.create(
                user=user,
                company_name=form.cleaned_data['company_name'],
                industry=form.cleaned_data['industry'],
                website=form.cleaned_data['website'],
                location=form.cleaned_data['location'],
                description=form.cleaned_data['description']
            )
            login(request, user)
            messages.success(request, "Company registration successful.")
            return redirect('company_portal:dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    return render(request, 'accounts/register_company.html')
