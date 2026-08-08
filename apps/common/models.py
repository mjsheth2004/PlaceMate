from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=10, unique=True, blank=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class PlacementDrive(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed'),
    ]

    company = models.ForeignKey('company_portal.CompanyProfile', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    job_description = models.TextField()
    salary_package = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    eligible_departments = models.ManyToManyField(Department)
    min_cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    max_backlogs = models.PositiveSmallIntegerField(default=0)
    eligible_passing_year = models.PositiveIntegerField()
    required_skills = models.ManyToManyField(Skill, blank=True)
    application_deadline = models.DateTimeField()
    interview_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    approved_by = models.ForeignKey('admin_portal.OfficerProfile', blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.company.company_name}"
