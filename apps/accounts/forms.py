from django import forms
from apps.accounts.models import User
from apps.student_portal.models import StudentProfile
from apps.company_portal.models import CompanyProfile
from apps.common.models import Department

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

    def clean_roll_number(self):
        roll_number = self.cleaned_data.get('roll_number')
        if StudentProfile.objects.filter(roll_number=roll_number).exists():
            raise forms.ValidationError("Roll number already registered.")
        return roll_number

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
