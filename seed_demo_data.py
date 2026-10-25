"""
Seed script to populate PlaceMate with demo data for faculty presentation.
Populates:
1. Students: Mayank, Sneh, Shabbir, Dhruv (and verifies Mrunal Sheth)
2. Companies: Omega Nova, Gateway Group, Techlab Innovations, TatvaSoft
3. Placement Drives: 4 published drives with future deadlines + eligibility criteria matching students
4. Applications: Rich, varied application states for all users to showcase analytics, status flows, and company dashboards
"""

import os
import django
from datetime import timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from apps.accounts.models import User
from apps.common.models import Department, Skill, PlacementDrive
from apps.student_portal.models import StudentProfile, Application
from apps.student_portal.signals import send_application_status_update_email, track_previous_status
from apps.company_portal.models import CompanyProfile
from apps.admin_portal.models import OfficerProfile

# Temporarily disconnect email notification signals during batch seed
try:
    post_save.disconnect(send_application_status_update_email, sender=Application)
    pre_save.disconnect(track_previous_status, sender=Application)
except Exception:
    pass

def seed_data():
    print("=" * 60)
    print("Starting PlaceMate Database Seeding for Faculty Demo")
    print("=" * 60)

    # 1. Departments
    dept_names = [
        ("Information Technology", "IT"),
        ("Computer Engineering", "CE"),
        ("Computer Science & Engineering", "CSE"),
        ("Electronics & Communication", "EC"),
        ("Mechanical Engineering", "ME"),
    ]
    dept_map = {}
    for name, code in dept_names:
        dept, _ = Department.objects.get_or_create(name=name, defaults={'code': code})
        dept_map[name] = dept
    print(f"[OK] Departments ready: {list(dept_map.keys())}")

    it_dept = dept_map["Information Technology"]
    ce_dept = dept_map["Computer Engineering"]
    cse_dept = dept_map["Computer Science & Engineering"]
    all_tech_depts = [it_dept, ce_dept, cse_dept]

    # 2. Skills
    skills_list = [
        "Python", "Django", "JavaScript", "React", "Node.js", "TypeScript",
        "SQL", "PostgreSQL", "Machine Learning", "Data Structures",
        "Algorithms", "HTML/CSS", "AWS", "Docker", "Git & GitHub", "Java", "C++"
    ]
    skill_map = {}
    for sk in skills_list:
        skill_obj, _ = Skill.objects.get_or_create(name=sk)
        skill_map[sk] = skill_obj
    print(f"[OK] Skills ready ({len(skill_map)} total)")

    # 3. Placement Officer
    officer_user, created = User.objects.get_or_create(
        email="infoplacemate@gmail.com",
        defaults={
            'role': User.OFFICER,
            'is_staff': True,
            'is_superuser': True,
            'email_verified': True,
            'first_name': "Placement",
            'last_name': "Officer"
        }
    )
    if created:
        officer_user.set_password("Admin@123")
        officer_user.save()
    else:
        officer_user.role = User.OFFICER
        officer_user.is_staff = True
        officer_user.email_verified = True
        officer_user.save()

    officer_profile, _ = OfficerProfile.objects.get_or_create(
        user=officer_user,
        defaults={
            'full_name': "Prof. Rajesh Verma",
            'designation': "Head of Training & Placement Cell"
        }
    )
    print(f"[OK] Officer profile ready: {officer_profile.full_name}")

    # 4. Verify & Update existing primary student (Mrunal Sheth)
    mrunal_user = User.objects.filter(email="mjsheth0711@gmail.com").first()
    if mrunal_user:
        mrunal_user.email_verified = True
        mrunal_user.save()
        mrunal_profile, _ = StudentProfile.objects.get_or_create(
            user=mrunal_user,
            defaults={
                'full_name': "Mrunal Sheth",
                'roll_number': "A38",
                'university': "GLS University",
                'department': it_dept,
                'semester': 7,
                'cgpa': Decimal("8.60"),
                'passing_year': 2028,
                'active_backlogs': 0,
                'is_verified': True,
                'resume': "resumes/Mrunal_Sheth_Resume.pdf",
                'profile_photo': "profile_photos/profile.png"
            }
        )
        mrunal_profile.is_verified = True
        mrunal_profile.department = it_dept
        mrunal_profile.passing_year = 2028
        mrunal_profile.semester = 7
        mrunal_profile.cgpa = Decimal("8.60")
        mrunal_profile.active_backlogs = 0
        if not mrunal_profile.resume:
            mrunal_profile.resume = "resumes/Mrunal_Sheth_Resume.pdf"
        if not mrunal_profile.profile_photo:
            mrunal_profile.profile_photo = "profile_photos/profile.png"
        mrunal_profile.save()
        mrunal_skills = [skill_map[s] for s in ["Python", "Django", "React", "SQL", "Machine Learning", "Data Structures", "Git & GitHub"] if s in skill_map]
        mrunal_profile.skills.set(mrunal_skills)
        print(f"[OK] Updated primary student: {mrunal_profile.full_name} ({mrunal_user.email})")
    else:
        mrunal_profile = None

    # 5. Add Students: Mayank, Sneh, Shabbir, Dhruv
    students_data = [
        {
            "name": "Mayank Patel",
            "email": "mayank@placemate.com",
            "roll": "A42",
            "dept": it_dept,
            "sem": 7,
            "cgpa": Decimal("8.75"),
            "year": 2028,
            "backlogs": 0,
            "resume": "resumes/Mayank_Patel_Resume.pdf",
            "skills": ["Python", "Django", "SQL", "React", "Git & GitHub", "Data Structures"]
        },
        {
            "name": "Sneh Shah",
            "email": "sneh@placemate.com",
            "roll": "A15",
            "dept": it_dept,
            "sem": 7,
            "cgpa": Decimal("9.10"),
            "year": 2028,
            "backlogs": 0,
            "resume": "resumes/Sneh_Shah_Resume.pdf",
            "skills": ["Python", "Machine Learning", "SQL", "Algorithms", "C++", "PostgreSQL"]
        },
        {
            "name": "Shabbir Husain",
            "email": "shabbir@placemate.com",
            "roll": "A21",
            "dept": ce_dept,
            "sem": 7,
            "cgpa": Decimal("8.40"),
            "year": 2028,
            "backlogs": 0,
            "resume": "resumes/Shabbir_Husain_Resume.pdf",
            "skills": ["JavaScript", "React", "Node.js", "TypeScript", "HTML/CSS", "Git & GitHub"]
        },
        {
            "name": "Dhruv Dave",
            "email": "dhruv@placemate.com",
            "roll": "A28",
            "dept": it_dept,
            "sem": 7,
            "cgpa": Decimal("8.25"),
            "year": 2028,
            "backlogs": 0,
            "resume": "resumes/Dhruv_Dave_Resume.pdf",
            "skills": ["Java", "SQL", "AWS", "Docker", "Data Structures", "Algorithms"]
        },
    ]

    student_profiles = []
    if mrunal_profile:
        student_profiles.append(mrunal_profile)

    for s in students_data:
        user, u_created = User.objects.get_or_create(
            email=s["email"],
            defaults={
                'role': User.STUDENT,
                'email_verified': True,
                'first_name': s["name"].split()[0],
                'last_name': s["name"].split()[-1] if len(s["name"].split()) > 1 else ""
            }
        )
        if u_created or not user.has_usable_password():
            user.set_password("Student@123")
            user.role = User.STUDENT
            user.email_verified = True
            user.save()

        sp, _ = StudentProfile.objects.get_or_create(
            user=user,
            defaults={
                'full_name': s["name"],
                'roll_number': s["roll"],
                'university': "GLS University",
                'department': s["dept"],
                'semester': s["sem"],
                'cgpa': s["cgpa"],
                'passing_year': s["year"],
                'active_backlogs': s["backlogs"],
                'is_verified': True,
                'resume': s["resume"],
                'profile_photo': "profile_photos/profile.png"
            }
        )
        # Ensure values
        sp.full_name = s["name"]
        sp.roll_number = s["roll"]
        sp.department = s["dept"]
        sp.semester = s["sem"]
        sp.cgpa = s["cgpa"]
        sp.passing_year = s["year"]
        sp.active_backlogs = s["backlogs"]
        sp.is_verified = True
        sp.resume = s["resume"]
        sp.profile_photo = "profile_photos/profile.png"
        sp.save()

        s_skills = [skill_map[sk] for sk in s["skills"] if sk in skill_map]
        sp.skills.set(s_skills)
        student_profiles.append(sp)
        print(f"[OK] Student profile ready: {sp.full_name} ({user.email}) - Roll: {sp.roll_number}")

    # 6. Add Companies: Omega Nova, Gateway, Techlab, TatvaSoft
    companies_data = [
        {
            "name": "Omega Nova Technologies",
            "email": "omega@placemate.com",
            "industry": "Enterprise Software & Cloud Platforms",
            "website": "https://www.omeganova.io",
            "location": "Ahmedabad, Gujarat",
            "logo": "company_logos/omega_nova.png",
            "description": "Omega Nova is a premier product engineering and enterprise SaaS development powerhouse, building high-throughput cloud architectures and AI-driven workflow platforms."
        },
        {
            "name": "Gateway Group",
            "email": "gateway@placemate.com",
            "industry": "IT Consulting & Digital Transformation",
            "website": "https://www.gatewaygroup.com",
            "location": "Ahmedabad / Pune",
            "logo": "company_logos/gateway.png",
            "description": "Gateway Group is an international information technology services and enterprise consulting company delivering state-of-the-art technology solutions across 30+ countries globally."
        },
        {
            "name": "Techlab Innovations",
            "email": "techlab@placemate.com",
            "industry": "FinTech & Data Engineering",
            "website": "https://www.techlabinnovations.com",
            "location": "GIFT City, Gandhinagar",
            "logo": "company_logos/techlab.png",
            "description": "Techlab Innovations specializes in next-generation financial technology, high-frequency transaction engines, and machine learning analytics for capital markets."
        },
        {
            "name": "TatvaSoft Software",
            "email": "tatvasoft@placemate.com",
            "industry": "Custom Enterprise Software & Web",
            "website": "https://www.tatvasoft.com",
            "location": "Ahmedabad, Gujarat",
            "logo": "company_logos/tatvasoft.png",
            "description": "TatvaSoft is a CMMi Level 3 certified global software development company delivering enterprise web, cloud, and mobile solutions for leading Fortune 500 enterprises."
        },
    ]

    company_profiles = {}
    for c in companies_data:
        c_user, c_created = User.objects.get_or_create(
            email=c["email"],
            defaults={
                'role': User.COMPANY,
                'email_verified': True,
                'first_name': c["name"]
            }
        )
        if c_created or not c_user.has_usable_password():
            c_user.set_password("Company@123")
            c_user.role = User.COMPANY
            c_user.email_verified = True
            c_user.save()

        cp, _ = CompanyProfile.objects.get_or_create(
            user=c_user,
            defaults={
                'company_name': c["name"],
                'industry': c["industry"],
                'website': c["website"],
                'location': c["location"],
                'logo': c["logo"],
                'description': c["description"],
                'is_verified': True
            }
        )
        cp.company_name = c["name"]
        cp.industry = c["industry"]
        cp.website = c["website"]
        cp.location = c["location"]
        cp.logo = c["logo"]
        cp.description = c["description"]
        cp.is_verified = True
        cp.save()
        company_profiles[c["name"]] = cp
        print(f"[OK] Company profile ready: {cp.company_name} ({c_user.email})")

    # 7. Add Placement Drives
    now = timezone.now()
    drives_data = [
        {
            "company": company_profiles["Omega Nova Technologies"],
            "title": "Full Stack Developer (Django + React)",
            "salary": Decimal("11.50"),
            "location": "Ahmedabad (Hybrid)",
            "min_cgpa": Decimal("7.50"),
            "max_backlogs": 0,
            "passing_year": 2028,
            "deadline": now + timedelta(days=20),
            "interview_date": now + timedelta(days=25),
            "skills": ["Python", "Django", "React", "SQL", "Git & GitHub"],
            "desc": (
                "Omega Nova is recruiting Full Stack Engineers for our Core Platform team.\n\n"
                "Key Responsibilities:\n"
                "- Develop end-to-end features using Django REST framework and React\n"
                "- Architect scalable database models with PostgreSQL\n"
                "- Integrate secure authentication and cloud microservices\n\n"
                "Compensation & Benefits:\n"
                "- 11.50 LPA starting package\n"
                "- Comprehensive health coverage & learning stipend\n"
                "- Hybrid working flexibility"
            )
        },
        {
            "company": company_profiles["Gateway Group"],
            "title": "Cloud & DevOps Associate Engineer",
            "salary": Decimal("8.80"),
            "location": "Ahmedabad",
            "min_cgpa": Decimal("7.00"),
            "max_backlogs": 0,
            "passing_year": 2028,
            "deadline": now + timedelta(days=18),
            "interview_date": now + timedelta(days=22),
            "skills": ["AWS", "Docker", "Python", "SQL", "Data Structures"],
            "desc": (
                "Gateway Group is looking for talented Cloud & DevOps Associates.\n\n"
                "Key Responsibilities:\n"
                "- Implement and maintain AWS infrastructure & Docker container clusters\n"
                "- Configure CI/CD automated deployment pipelines\n"
                "- Monitor uptime, performance metrics, and system security\n\n"
                "Benefits:\n"
                "- 8.80 LPA package + performance appraisal bonus\n"
                "- Fast-track training and AWS certification mentorship"
            )
        },
        {
            "company": company_profiles["Techlab Innovations"],
            "title": "AI & Data Intelligence Specialist",
            "salary": Decimal("13.20"),
            "location": "GIFT City, Gandhinagar",
            "min_cgpa": Decimal("8.00"),
            "max_backlogs": 0,
            "passing_year": 2028,
            "deadline": now + timedelta(days=24),
            "interview_date": now + timedelta(days=28),
            "skills": ["Python", "Machine Learning", "SQL", "Algorithms", "PostgreSQL"],
            "desc": (
                "Join Techlab's Advanced Analytics team in the prestigious GIFT City financial hub.\n\n"
                "Key Responsibilities:\n"
                "- Build predictive ML pipelines for high-frequency transactional data\n"
                "- Design ETL data flows using Python and modern data stores\n"
                "- Produce executive analytical insights and visual dashboards\n\n"
                "Package Details:\n"
                "- 13.20 LPA fixed package + ESOP incentives\n"
                "- Free transportation from Ahmedabad & corporate wellness"
            )
        },
        {
            "company": company_profiles["TatvaSoft Software"],
            "title": "Associate Software Engineer (Web & Mobile)",
            "salary": Decimal("7.50"),
            "location": "Ahmedabad, Gujarat",
            "min_cgpa": Decimal("7.00"),
            "max_backlogs": 0,
            "passing_year": 2028,
            "deadline": now + timedelta(days=26),
            "interview_date": now + timedelta(days=30),
            "skills": ["JavaScript", "React", "Java", "HTML/CSS", "SQL"],
            "desc": (
                "TatvaSoft is welcoming enthusiastic software engineers for client enterprise solutions.\n\n"
                "Key Responsibilities:\n"
                "- Develop responsive web components and frontend applications\n"
                "- Write maintainable code following agile best practices\n"
                "- Collaborate with QA and UX teams for seamless deployments\n\n"
                "Benefits:\n"
                "- 7.50 LPA starting package with 6-month growth review"
            )
        },
        {
            # Drive 5: Omega Nova SDE-1 Core Platform.
            # Intentionally left UNAPPLIED by Mrunal so it displays under "Eligible Placement Drives" on Mrunal's dashboard!
            "company": company_profiles["Omega Nova Technologies"],
            "title": "Software Development Engineer - Core Platform (SDE-1)",
            "salary": Decimal("10.00"),
            "location": "Ahmedabad / Hybrid",
            "min_cgpa": Decimal("7.50"),
            "max_backlogs": 0,
            "passing_year": 2028,
            "deadline": now + timedelta(days=30),
            "interview_date": now + timedelta(days=35),
            "skills": ["Python", "SQL", "Data Structures", "Algorithms", "Git & GitHub"],
            "desc": (
                "Omega Nova Core Platform team is expanding!\n\n"
                "Key Responsibilities:\n"
                "- Build microservices handling millions of monthly API requests\n"
                "- Implement secure API gateways, caching, and rate limiters\n"
                "- Optimize database queries and schema performance\n\n"
                "Eligible candidates can apply directly through the PlaceMate portal."
            )
        },
        {
            # Drive 6: Gateway Group Cybersecurity & Infrastructure Analyst
            # Intentionally left UNAPPLIED by Mrunal so it displays under "Eligible Placement Drives" on Mrunal's dashboard!
            "company": company_profiles["Gateway Group"],
            "title": "Cybersecurity & Infrastructure Analyst",
            "salary": Decimal("9.20"),
            "location": "Ahmedabad / Pune",
            "min_cgpa": Decimal("7.00"),
            "max_backlogs": 0,
            "passing_year": 2028,
            "deadline": now + timedelta(days=28),
            "interview_date": now + timedelta(days=32),
            "skills": ["AWS", "Docker", "Python", "SQL", "Git & GitHub"],
            "desc": (
                "Gateway Group is hiring a Cybersecurity & Infrastructure Analyst to safeguard our global enterprise deployments.\n\n"
                "Key Responsibilities:\n"
                "- Perform vulnerability scans, security audits, and penetration testing on cloud nodes\n"
                "- Implement IAM roles, encryption standards, and compliance frameworks\n"
                "- Work with DevOps teams to secure CI/CD build environments"
            )
        }
    ]

    placement_drives = []
    for d in drives_data:
        drive, created = PlacementDrive.objects.get_or_create(
            company=d["company"],
            title=d["title"],
            defaults={
                'job_description': d["desc"],
                'salary_package': d["salary"],
                'location': d["location"],
                'min_cgpa': d["min_cgpa"],
                'max_backlogs': d["max_backlogs"],
                'eligible_passing_year': d["passing_year"],
                'application_deadline': d["deadline"],
                'interview_date': d["interview_date"],
                'status': 'published',
                'approved_by': officer_profile
            }
        )
        # Update fields to ensure fresh deadlines and published state
        drive.job_description = d["desc"]
        drive.salary_package = d["salary"]
        drive.location = d["location"]
        drive.min_cgpa = d["min_cgpa"]
        drive.max_backlogs = d["max_backlogs"]
        drive.eligible_passing_year = d["passing_year"]
        drive.application_deadline = d["deadline"]
        drive.interview_date = d["interview_date"]
        drive.status = 'published'
        drive.approved_by = officer_profile
        drive.save()

        drive.eligible_departments.set(all_tech_depts)
        d_skills = [skill_map[sk] for sk in d["skills"] if sk in skill_map]
        drive.required_skills.set(d_skills)
        placement_drives.append(drive)
        print(f"[OK] Placement Drive ready: '{drive.title}' at {drive.company.company_name} (Deadline: {drive.application_deadline.strftime('%b %d, %Y')})")

    # 8. Create Applications
    drive_0 = placement_drives[0]
    drive_1 = placement_drives[1]
    drive_2 = placement_drives[2]
    drive_3 = placement_drives[3]
    drive_4 = placement_drives[4]
    drive_5 = placement_drives[5]

    # Student lookup by name
    student_by_name = {sp.full_name: sp for sp in student_profiles}

    # Ensure Mrunal does NOT have an application on drive_3, drive_4, drive_5 so Mrunal has 3 eligible drives ready to apply on dashboard
    if mrunal_profile:
        Application.objects.filter(student=mrunal_profile, drive__in=[drive_3, drive_4, drive_5]).delete()

    app_matrix = [
        # Drive 0: Omega Nova Full Stack (11.5 LPA)
        ("Mrunal Sheth", drive_0, "shortlisted"),
        ("Mayank Patel", drive_0, "interview_scheduled"),
        ("Sneh Shah", drive_0, "selected"),
        ("Shabbir Husain", drive_0, "applied"),
        ("Dhruv Dave", drive_0, "shortlisted"),

        # Drive 1: Gateway Group Cloud & DevOps (8.8 LPA)
        ("Mrunal Sheth", drive_1, "interview_scheduled"),
        ("Mayank Patel", drive_1, "selected"),
        ("Sneh Shah", drive_1, "shortlisted"),
        ("Shabbir Husain", drive_1, "interview_scheduled"),
        ("Dhruv Dave", drive_1, "applied"),

        # Drive 2: Techlab Innovations AI & Data (13.2 LPA)
        ("Mrunal Sheth", drive_2, "applied"),
        ("Mayank Patel", drive_2, "shortlisted"),
        ("Sneh Shah", drive_2, "selected"),
        ("Shabbir Husain", drive_2, "applied"),
        ("Dhruv Dave", drive_2, "interview_scheduled"),

        # Drive 3: TatvaSoft Web & Mobile (7.5 LPA) - Unapplied by Mrunal
        ("Mayank Patel", drive_3, "applied"),
        ("Sneh Shah", drive_3, "applied"),
        ("Shabbir Husain", drive_3, "selected"),
        ("Dhruv Dave", drive_3, "shortlisted"),

        # Drive 4: Omega Nova Core Platform (10.0 LPA) - Unapplied by Mrunal
        ("Mayank Patel", drive_4, "applied"),
        ("Sneh Shah", drive_4, "shortlisted"),
        ("Shabbir Husain", drive_4, "applied"),
        ("Dhruv Dave", drive_4, "applied"),

        # Drive 5: Gateway Group Cybersecurity (9.20 LPA) - Unapplied by Mrunal
        ("Mayank Patel", drive_5, "interview_scheduled"),
        ("Sneh Shah", drive_5, "shortlisted"),
        ("Shabbir Husain", drive_5, "applied"),
        ("Dhruv Dave", drive_5, "selected"),
    ]

    applied_count = 0
    for student_name, drive_obj, status_choice in app_matrix:
        sp = student_by_name.get(student_name)
        if sp:
            app, _ = Application.objects.get_or_create(
                student=sp,
                drive=drive_obj,
                defaults={'status': status_choice}
            )
            app.status = status_choice
            app.save()
            applied_count += 1

    print(f"[OK] Seeded {applied_count} student applications with full lifecycle statuses")
    print("=" * 60)
    print("Database seeding successfully completed!")
    print("=" * 60)

if __name__ == '__main__':
    seed_data()
