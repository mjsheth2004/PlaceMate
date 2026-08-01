# 01_SRS.md — Software Requirements Specification

## Placement Management Portal

**Document Version:** 1.0
**Project Type:** Django-based Web Application (College Academic Project)

---

## 1. Introduction

### 1.1 Purpose

This document specifies the functional and non-functional requirements
for the **Placement Management Portal**, a Django-based web application
that digitizes the campus recruitment lifecycle. It is intended to guide
development, serve as a reference for evaluators/faculty, and act as the
baseline against which the system will be tested (see `09_Testing.md`).

### 1.2 Scope

The system connects three user roles — **Students**, **Companies/HR**,
and **Placement Officers (Admin)** — on a single platform to manage
profiles, eligibility, applications, interviews, results, and reporting.
It replaces manual, spreadsheet- and email-driven placement processes
with a centralized, role-based web application.

Detailed scope tiering (MVP / Stretch / Future Enhancements) is
maintained in `02_Project_Requirements.md`; this document focuses on
*what* the system must do, not *when* each piece is delivered.

### 1.3 Definitions, Acronyms, Abbreviations

| Term | Meaning |
|---|---|
| SRS | Software Requirements Specification |
| CGPA | Cumulative Grade Point Average |
| RBAC | Role-Based Access Control |
| FR | Functional Requirement |
| NFR | Non-Functional Requirement |
| Drive | A placement/recruitment event created by a company for a set of eligible students |
| Backlog | A pending/failed academic subject a student has not yet cleared |
| ORM | Object-Relational Mapping (Django's database abstraction layer) |

### 1.4 References

- `02_Project_Requirements.md` — scope tiers and feature prioritization
- `03_Architecture.md` — system and app-level architecture
- `08_Database_Design.md` — schema and entity relationships
- `09_Testing.md` — test plan and cases derived from this SRS

### 1.5 Document Overview

Section 2 describes the product at a high level. Section 3 lists
functional requirements grouped by module, each with a traceable ID.
Section 4 covers interface requirements. Section 5 covers non-functional
requirements. Section 6 covers other constraints.

---

## 2. Overall Description

### 2.1 Product Perspective

The Placement Management Portal is a standalone, self-contained web
application. It is not a replacement for institutional ERP systems but
is designed to interoperate with them at a basic level (e.g., exporting
reports that could be shared with administration).

### 2.2 Product Functions (Summary)

- Role-based registration and authentication (Student / Company / Officer)
- Student profile, resume, and skills management
- Company and job-drive management
- Automated eligibility checking against drive criteria
- Application lifecycle tracking (Applied → Shortlisted → Interview → Result)
- Interview scheduling
- Result publication
- Notifications (drive announcements, reminders, results)
- Dashboards for each role
- Report generation and export (PDF/Excel)

### 2.3 User Classes and Characteristics

| Role | Description | Technical Proficiency |
|---|---|---|
| Student | End user applying to drives | Low–Medium |
| Company/HR | Posts drives, reviews applicants | Low–Medium |
| Placement Officer (Admin) | Manages the entire platform | Medium |

### 2.4 Operating Environment

- **Backend:** Django 6.7.0 (Python)
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript (server-rendered templates)
- **Charts:** Chart.js
- **PDF Generation:** WeasyPrint / ReportLab
- **Excel Export:** openpyxl
- **Deployment targets:** Render / Railway / PythonAnywhere
- **Client:** Any modern web browser (desktop or mobile), no native app required

### 2.5 Design and Implementation Constraints

- Must use Django's built-in authentication system, extended via a
  custom user model to support three roles (Student, Company, Officer).
- File uploads (resumes, logos, photos) are restricted to defined
  formats and size limits (see FR-STU-04, FR-STU-05).
- Must be built to run within a single semester/hackathon timeline as
  an academic project; architecture should stay simple enough for a
  small team to implement and defend.

### 2.6 Assumptions and Dependencies

- Users have access to a stable internet connection.
- Institutional data (department list, academic calendar) is entered
  manually by the Placement Officer; no live integration with a
  college ERP is assumed for MVP.
- Email delivery (for verification/notifications) depends on a
  third-party SMTP provider or service (e.g., Gmail SMTP, SendGrid).

---

## 3. Functional Requirements

Each requirement has an ID of the form `FR-<MODULE>-<NUMBER>` for
traceability into `09_Testing.md`. Priority: **M**ust-have,
**S**hould-have, **C**ould-have — cross-check against the MVP/Stretch/
Future tiers in `02_Project_Requirements.md`.

### 3.1 Authentication Module (AUTH)

| ID | Requirement | Priority |
|---|---|---|
| FR-AUTH-01 | System shall allow Students, Companies, and Placement Officers to register with role-specific fields. | M |
| FR-AUTH-02 | System shall allow all roles to log in using email and password. | M |
| FR-AUTH-03 | System shall verify a user's email address before granting full access. | S |
| FR-AUTH-04 | System shall provide a "Forgot Password" flow using a time-limited reset link. | M |
| FR-AUTH-05 | System shall enforce role-based access control (RBAC), restricting each dashboard and view to its intended role. | M |
| FR-AUTH-06 | System shall log a user out after a defined period of inactivity. | C |

### 3.2 Student Module (STU)

| ID | Requirement | Priority |
|---|---|---|
| FR-STU-01 | Student shall be able to create and edit a profile (name, roll number, university, department, semester, CGPA). | M |
| FR-STU-02 | Student shall be able to add/edit/remove skills and projects. | M |
| FR-STU-03 | Student shall be able to add certifications. | S |
| FR-STU-04 | Student shall be able to upload a resume in PDF format (max size enforced, e.g., 5 MB). | M |
| FR-STU-05 | Student shall be able to upload a profile photo (JPEG/PNG, max size enforced). | S |
| FR-STU-06 | System shall display a profile-completion percentage to the student. | S |
| FR-STU-07 | Student shall be able to view a list of placement drives they are eligible for. | M |
| FR-STU-08 | Student shall be able to apply to an eligible drive. | M |
| FR-STU-09 | Student shall be able to track the status of each application (Applied, Shortlisted, Interview Scheduled, Selected, Rejected). | M |
| FR-STU-10 | Student shall be able to view scheduled interview date, time, venue, and panel for drives they've progressed in. | M |
| FR-STU-11 | Student shall receive notifications for drive announcements, interview reminders, results, and deadlines. | M |
| FR-STU-12 | Student shall be able to view their historical placement record after being marked as selected. | S |

### 3.3 Placement Officer / Admin Module (ADM)

| ID | Requirement | Priority |
|---|---|---|
| FR-ADM-01 | Officer shall be able to view, verify, and manage all student profiles. | M |
| FR-ADM-02 | Officer shall be able to add, edit, and remove company records. | M |
| FR-ADM-03 | Officer shall be able to create placement drives on behalf of or alongside companies. | M |
| FR-ADM-04 | Officer shall be able to define/override eligibility criteria for a drive (CGPA, department, backlog limits). | M |
| FR-ADM-05 | System shall automatically flag eligible vs. ineligible students per drive based on defined criteria. | M |
| FR-ADM-06 | Officer shall be able to schedule and modify interview slots. | M |
| FR-ADM-07 | Officer shall be able to publish final results (Selected / Waiting List / Rejected). | M |
| FR-ADM-08 | Officer shall be able to generate and export reports (student, company, department-wise, year-wise, salary) as PDF or Excel. | M |
| FR-ADM-09 | Officer shall be able to view aggregate analytics: total students, total companies, placement %, highest package, average package, upcoming drives. | M |
| FR-ADM-10 | Officer shall be able to send manual notifications/announcements to students. | S |

### 3.4 Company / HR Module (CMP)

| ID | Requirement | Priority |
|---|---|---|
| FR-CMP-01 | Company shall be able to register and log in. | M |
| FR-CMP-02 | Company shall be able to create a recruitment drive with job description, salary package, location, and eligibility criteria. | M |
| FR-CMP-03 | Company shall be able to view the list of applicants for their drive(s). | M |
| FR-CMP-04 | Company shall be able to download applicant resumes. | M |
| FR-CMP-05 | Company shall be able to shortlist candidates from the applicant pool. | M |
| FR-CMP-06 | Company shall be able to propose/confirm interview schedules. | M |
| FR-CMP-07 | Company shall be able to publish final selection results for their drive. | M |
| FR-CMP-08 | Company shall be able to view a dashboard summarizing applications received, eligible candidates, shortlisted, and selected counts. | S |

### 3.5 Eligibility Checker (ELG)

| ID | Requirement | Priority |
|---|---|---|
| FR-ELG-01 | System shall validate student eligibility against a drive's minimum CGPA. | M |
| FR-ELG-02 | System shall validate eligibility against department restrictions. | M |
| FR-ELG-03 | System shall validate eligibility against passing year. | M |
| FR-ELG-04 | System shall validate eligibility against active backlog count. | M |
| FR-ELG-05 | System shall validate eligibility against required skills, where specified. | S |
| FR-ELG-06 | System shall prevent ineligible students from applying to a drive at the UI and API/view level. | M |

### 3.6 Notifications (NTF)

| ID | Requirement | Priority |
|---|---|---|
| FR-NTF-01 | System shall notify eligible students when a new drive is announced. | M |
| FR-NTF-02 | System shall send interview reminders ahead of scheduled interviews. | S |
| FR-NTF-03 | System shall notify students when results are published. | M |
| FR-NTF-04 | System shall notify students of upcoming application deadlines. | S |
| FR-NTF-05 | Notifications shall be deliverable via in-app alerts, with email as an optional channel. | S |

### 3.7 Reports & Analytics (RPT)

| ID | Requirement | Priority |
|---|---|---|
| FR-RPT-01 | System shall generate a student report (profile + application history). | M |
| FR-RPT-02 | System shall generate a company-wise report of drives and outcomes. | S |
| FR-RPT-03 | System shall generate department-wise and year-wise placement statistics. | M |
| FR-RPT-04 | System shall generate a salary/package report across selected students. | S |
| FR-RPT-05 | All reports shall be exportable in both PDF and Excel formats. | M |

---

## 4. External Interface Requirements

### 4.1 User Interfaces

- Responsive, browser-based UI using server-rendered Django templates
  (HTML/CSS/JS), usable on both desktop and mobile viewports.
- Three distinct dashboard layouts (Student, Company, Officer), sharing
  a common visual design system and navigation shell (`templates/shared/`).
- Charts rendered client-side via Chart.js on dashboard and report views.

### 4.2 Hardware Interfaces

None beyond a standard client device (desktop/laptop/mobile) capable of
running a modern web browser. No specialized hardware is required.

### 4.3 Software Interfaces

| Interface | Purpose |
|---|---|
| PostgreSQL | Primary relational data store, accessed via Django ORM |
| SMTP provider | Outbound email for verification and notifications |
| WeasyPrint / ReportLab | Server-side PDF generation for reports and resumes rendering |
| openpyxl | Server-side Excel (.xlsx) report export |
| Chart.js (CDN or bundled) | Client-side chart rendering |

### 4.4 Communication Interfaces

- Standard HTTPS for all client-server communication.
- Email (SMTP) for verification links, password resets, and optional
  notification delivery.

---

## 5. Non-Functional Requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-01 | Performance | Common pages (dashboards, drive listings) should load within 2–3 seconds under normal load for a single-institution deployment. |
| NFR-02 | Security | Passwords shall be stored using Django's default hashing (PBKDF2 or stronger); never stored in plaintext. |
| NFR-03 | Security | File uploads shall be validated for type and size server-side, not just client-side. |
| NFR-04 | Security | RBAC shall be enforced at the view/permission level, not only hidden in the UI. |
| NFR-05 | Usability | Core workflows (apply to a drive, check status, publish results) shall be completable within 3 clicks from the respective dashboard. |
| NFR-06 | Reliability | The system shall handle invalid form input gracefully with clear validation messages, without exposing stack traces to end users. |
| NFR-07 | Maintainability | Code shall be organized by Django app per role/domain (see project structure), enabling independent development and testing of each module. |
| NFR-08 | Scalability | Database queries for listing/filtering (students, drives, applications) shall use pagination to remain performant as record counts grow. |
| NFR-09 | Portability | The application shall be deployable on at least one of Render, Railway, or PythonAnywhere without code changes, using environment-based configuration (`.env`). |
| NFR-10 | Auditability | Key state transitions (application status changes, result publication) should be timestamped for traceability. |

---

## 6. Other Requirements

### 6.1 Database Requirements

Detailed schema, entity-relationship design, and table definitions are
maintained separately in `08_Database_Design.md`. At minimum, the
system requires persistent storage for: Users, Students, Companies,
PlacementDrives, Applications, Interviews, Results, Notifications,
Skills, and Departments.

### 6.2 Legal / Compliance

- Student data (CGPA, contact info, resumes) is sensitive and should be
  accessible only to authorized roles (self, verifying Officer, and
  companies the student has explicitly applied to).
- No requirement for GDPR/DPDP-level compliance is assumed for this
  academic project, but basic data-access discipline (per NFR-02–04)
  should be followed as good practice.

### 6.3 Out of Scope (for this SRS)

- Payment processing (no fees are collected via the platform).
- Native mobile applications (web-responsive only).
- Real-time chat between students and recruiters.

*(Confirm against `02_Project_Requirements.md` if any of the above move
into scope for Stretch or Future tiers.)*

---

## 7. Appendix

### 7.1 Requirement ID Prefix Legend

| Prefix | Module |
|---|---|
| AUTH | Authentication |
| STU | Student |
| ADM | Placement Officer / Admin |
| CMP | Company / HR |
| ELG | Eligibility Checker |
| NTF | Notifications |
| RPT | Reports & Analytics |
| NFR | Non-Functional Requirement |

### 7.2 Traceability Note

Each FR/NFR ID in this document should map to at least one test case in
`09_Testing.md`. When requirements change, update the ID here first,
then propagate the change to the test plan and architecture doc.