import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from apps.common.models import Department
from apps.accounts.models import User
from apps.student_portal.models import StudentProfile

dept, _ = Department.objects.get_or_create(name="Computer Engineering", code="CE")

client = Client()
response = client.post('/accounts/register/student/', {
    'email': 'student2@example.com',
    'password': 'strongpassword123',
    'full_name': 'Test Student 2',
    'roll_number': '123457',
    'university': 'Test University',
    'department': dept.id,
    'semester': 6,
    'cgpa': 8.5,
    'passing_year': 2025,
    'active_backlogs': 0
})

assert response.status_code == 302 # redirect to login
user = User.objects.get(email='student2@example.com')
assert user.role == User.STUDENT
assert StudentProfile.objects.filter(user=user).exists()
print("Tests passed successfully!")
