# 🎓 PlaceMate - Placement Management Portal

[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Shared_DB-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

**PlaceMate** is a modern, responsive, role-based Placement Management System designed to streamline campus recruitment for educational institutions, students, and corporate recruiters. Built on Django, PlaceMate delivers a seamless, secure experience with strict separation of concerns, rich visual aesthetics, dark mode support, automated email notifications, and robust role-based access control (RBAC).

---

## 🌟 Key Features

### 👨‍🎓 Student Portal
* **Interactive Dashboard**: Real-time KPI metrics tracking eligible placement drives, submitted applications, scheduled interviews, and job offers.
* **Profile Completeness Indicator**: Visual completion progress bar prompting students to fill academic records, upload resumes, and set profile pictures.
* **Placement Drive Discovery**: Browse active campus recruitment opportunities filtered by minimum CGPA, backlog criteria, passing batch, and eligible department.
* **One-Click Application**: Check eligibility instantly and submit job applications.
* **Live Application Status Roster**: Track application progression (*Applied*, *Shortlisted*, *Interview Scheduled*, *Selected*, *Rejected*).
* **Profile & Document Lightbox**: Manage academic details, core skills, resume downloads, and full-screen profile photo lightbox modal.

---

### 🏢 Company / Recruiter Portal
* **Recruiter Metrics Dashboard**: Overview of active placement drives, candidate applicant counts, shortlisted candidates, and selections.
* **Drive Management System**: Create, update, publish, or archive recruitment drives with detailed descriptions, salary packages (LPA), locations, deadlines, and skill requirements.
* **Applicant Roster & Filter Engine**: Review candidate applications across all company drives with search (by candidate name, roll number, email) and multi-status filter controls.
* **Automated Status Workflow & Email Notifications**: Update applicant statuses directly from the roster with automated transactional email updates dispatched to candidates upon status changes.
* **One-Click Resume Access**: View and download candidate resumes directly from the recruiter dashboard.

---

### 🛡️ Core System & Architecture
* **Strict Architecture & Clean Separation**: 100% clean HTML templates with **zero inline CSS (`style="..."`)** and **zero inline JS handlers**, leveraging modular design system CSS and vanilla JavaScript.
* **Dark Mode & Responsive UI**: Smooth theme switching synchronized across user sessions with CSS custom properties.
* **Role-Based Access Control (RBAC)**: Custom user model (`accounts.User`) with dedicated decorators (`@student_required`, `@company_required`) and role-aware navigation.
* **Production Security Hardening**: Environment-driven configurations for SSL redirects, HSTS headers, secure cookies (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`), and Clickjacking (`X_FRAME_OPTIONS`) protection.

---

## 📁 Repository Structure

```
PlaceMate/
├── apps/
│   ├── accounts/          # Custom User model, authentication & role management
│   ├── student_portal/    # Student dashboard, profile management, and drive applications
│   ├── company_portal/    # Company profile, drive management & applicant roster
│   ├── admin_portal/      # Administrative operations
│   ├── common/            # Shared models (PlacementDrive, Department, Skill)
│   ├── notifications/     # Transactional email services
│   ├── reports/           # Placement analytics & reporting
│   └── api/               # External/internal endpoints
├── config/                # Django project settings & WSGI/ASGI configurations
├── static/                # Global and portal static assets (CSS tokens, JS scripts)
│   ├── css/               # Global theme tokens (theme.css)
│   ├── student_portal/    # Student portal stylesheets & scripts
│   └── company_portal/    # Recruiter portal stylesheets & scripts
├── templates/             # HTML5 Semantic templates
│   ├── accounts/
│   ├── student_portal/
│   ├── company_portal/
│   └── shared/            # Base templates & alert layouts
├── build.sh               # Production deployment build script
├── Procfile               # Gunicorn WSGI process configuration
├── manage.py
├── requirements.txt       # Project dependencies
└── README.md
```

---

## 🛠️ Tech Stack

* **Backend**: Python 3.10+, Django 6.0
* **Frontend**: HTML5, Vanilla CSS (Design Tokens & Utility Classes), Vanilla JavaScript (ES6 Modules)
* **Database**: SQLite (Development) / PostgreSQL via `dj-database-url` (Production)
* **WSGI & Static Server**: Gunicorn, WhiteNoise
* **Authentication & Mail**: Django Auth System, SMTP / Console Email Backends

---

## 🚀 Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/mjsheth2004/PlaceMate.git
cd PlaceMate
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```ini
SECRET_KEY=your-custom-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3

# Optional: Email Configuration for Live Testing
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
SITE_URL=http://127.0.0.1:8000
```

### 5. Apply Database Migrations & Seed Data
```bash
python manage.py migrate
python seed_skills.py
```

### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 7. Run Local Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your web browser.

---

## 🌐 Deploying to Production (Render / Railway / PythonAnywhere)

PlaceMate includes production-ready deployment scripts (`build.sh` and `Procfile`).

### Deploying on Render (Free Hosting)
1. Sign in to **[Render.com](https://render.com/)** with your GitHub account.
2. Click **New +** -> **Web Service** and select `mjsheth2004/PlaceMate`.
3. Set the following build options:
   * **Runtime**: `Python 3`
   * **Build Command**: `./build.sh`
   * **Start Command**: `gunicorn config.wsgi:application`
4. Add Environment Variables in Render:
   * `SECRET_KEY`: `<generate-a-strong-random-key>`
   * `DEBUG`: `False`
   * `ALLOWED_HOSTS`: `your-app-name.onrender.com`
5. Click **Create Web Service**.

---

## 🧪 Security & Verification

PlaceMate passes all production readiness checks:
```bash
# Run Django system deployment security check
DEBUG=False SECRET_KEY="your-prod-key" ALLOWED_HOSTS="yourdomain.com" python manage.py check --deploy
```
*Output: `System check identified no issues (0 silenced).`*

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
