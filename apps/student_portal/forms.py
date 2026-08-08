from django import forms
from .models import StudentProfile
from apps.common.models import Department, Skill

class StudentProfileForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(), 
        required=False, 
        widget=forms.SelectMultiple(attrs={'class': 'input-field', 'size': '5'})
    )

    class Meta:
        model = StudentProfile
        fields = [
            'full_name', 
            'roll_number', 
            'university', 
            'department', 
            'semester', 
            'cgpa', 
            'passing_year', 
            'active_backlogs', 
            'skills', 
            'resume', 
            'profile_photo'
        ]
        widgets = {
            'resume': forms.FileInput(attrs={'class': 'file-upload-input'}),
            'profile_photo': forms.FileInput(attrs={'class': 'file-upload-input'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply standard input classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['resume', 'profile_photo']:
                field.widget.attrs.update({'class': 'input-field'})
        
        # Make roll_number readonly since it's an primary identifier
        self.fields['roll_number'].widget.attrs['readonly'] = True
