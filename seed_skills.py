import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.common.models import Skill

skills = [
    "Python", "Java", "C++", "JavaScript", "React", 
    "Node.js", "Django", "SQL", "Machine Learning", 
    "Data Structures", "Algorithms", "HTML/CSS", "AWS"
]

for skill_name in skills:
    Skill.objects.get_or_create(name=skill_name)

print("Skills seeded successfully!")
