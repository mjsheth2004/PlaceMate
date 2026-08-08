from django import forms
from .models import CompanyProfile
from apps.common.models import PlacementDrive, Department, Skill

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'logo', 'industry', 'website', 'location', 'description']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'e.g. Acme Corporation'}),
            'industry': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'e.g. Software & Technology'}),
            'website': forms.URLInput(attrs={'class': 'input-field', 'placeholder': 'https://example.com'}),
            'location': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'e.g. Bengaluru, India'}),
            'description': forms.Textarea(attrs={'class': 'input-field', 'rows': 4, 'placeholder': 'Brief description of your company...'}),
            'logo': forms.FileInput(attrs={'class': 'input-field-file'}),
        }

class PlacementDriveForm(forms.ModelForm):
    eligible_departments = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'}),
        required=True
    )
    required_skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'}),
        required=False
    )
    application_deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'input-field'}),
        required=True
    )
    interview_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'input-field'}),
        required=False
    )

    class Meta:
        model = PlacementDrive
        fields = [
            'title', 'job_description', 'salary_package', 'location', 
            'eligible_departments', 'min_cgpa', 'max_backlogs', 
            'eligible_passing_year', 'required_skills', 'application_deadline', 
            'interview_date', 'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'e.g. Software Engineer Trainee'}),
            'job_description': forms.Textarea(attrs={'class': 'input-field', 'rows': 5, 'placeholder': 'Detailed job description, responsibilities, and requirements...'}),
            'salary_package': forms.NumberInput(attrs={'class': 'input-field', 'step': '0.01', 'placeholder': 'LPA e.g. 12.00'}),
            'location': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'e.g. Remote / Bengaluru'}),
            'min_cgpa': forms.NumberInput(attrs={'class': 'input-field', 'step': '0.1', 'min': '0.0', 'max': '10.0', 'placeholder': 'e.g. 6.5'}),
            'max_backlogs': forms.NumberInput(attrs={'class': 'input-field', 'min': '0', 'placeholder': 'e.g. 0'}),
            'eligible_passing_year': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'e.g. 2026'}),
            'status': forms.Select(attrs={'class': 'input-field'}),
        }
