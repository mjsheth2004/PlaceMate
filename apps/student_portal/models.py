from django.db import models

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.common.models import Department, Skill

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    roll_number = models.CharField(max_length=50, unique=True)
    university = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    semester = models.PositiveSmallIntegerField()
    cgpa = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        validators=[MinValueValidator(0.00), MaxValueValidator(10.00)]
    )
    passing_year = models.PositiveIntegerField()
    active_backlogs = models.PositiveSmallIntegerField(default=0)
    skills = models.ManyToManyField(Skill, blank=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    profile_photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.roll_number})"
