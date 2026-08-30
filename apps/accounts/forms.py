import re
from django import forms
from apps.accounts.models import User
from apps.student_portal.models import StudentProfile
from apps.company_portal.models import CompanyProfile
from apps.common.models import Department

def validate_password_strength(password):
    if not password or len(password) < 8:
        raise forms.ValidationError("Password must be at least 8 characters long.")
    if not re.search(r'[A-Z]', password):
        raise forms.ValidationError("Password must contain at least 1 capital letter (A-Z).")
    if not re.search(r'[a-zA-Z]', password):
        raise forms.ValidationError("Password must contain alphabetic letters.")
    if not re.search(r'\d', password):
        raise forms.ValidationError("Password must be a combination of alphabets and numbers (must include at least 1 number).")
    return password

class StudentRegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    full_name = forms.CharField(max_length=255)
    roll_number = forms.CharField(max_length=50)
    university = forms.CharField(max_length=255)
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    semester = forms.IntegerField(min_value=1, max_value=10)
    cgpa = forms.DecimalField(max_digits=4, decimal_places=2, min_value=0.00, max_value=10.00)
    passing_year = forms.IntegerField(min_value=2020, max_value=2030)
    active_backlogs = forms.IntegerField(min_value=0, required=False, initial=0)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return validate_password_strength(password)

    def clean(self):
        cleaned_data = super().clean()
        roll_number = cleaned_data.get('roll_number')
        department = cleaned_data.get('department')
        if roll_number and department:
            if StudentProfile.objects.filter(department=department, roll_number=roll_number).exists():
                self.add_error('roll_number', f"Roll number '{roll_number}' is already registered in {department.name}.")
        return cleaned_data

class CompanyRegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    company_name = forms.CharField(max_length=255)
    industry = forms.CharField(max_length=100, required=False)
    website = forms.URLField(required=False)
    location = forms.CharField(max_length=255, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return validate_password_strength(password)

