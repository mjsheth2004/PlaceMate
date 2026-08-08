# Placement Management Portal

## Overview

The **Placement Management Portal** is a Django-based web application
that digitizes the campus placement process. It enables students,
companies, and the placement cell to manage the entire recruitment
lifecycle from a single platform.

------------------------------------------------------------------------

# Problem Statement

Many colleges still manage placements manually using spreadsheets,
emails, and paper forms. This leads to:

-   Manual eligibility checking
-   Difficulty tracking applications
-   Scattered student records
-   Delayed communication
-   Time-consuming report generation

The Placement Management Portal automates these tasks to improve
efficiency, transparency, and accuracy.

------------------------------------------------------------------------

# Objectives

-   Digitize campus placement activities
-   Reduce manual work
-   Automate eligibility verification
-   Improve communication between students and recruiters
-   Generate reports and analytics
-   Provide a centralized placement database

------------------------------------------------------------------------

# User Roles

## Student

Students can:

-   Register/Login
-   Complete profile
-   Upload resume
-   Upload profile photo
-   Add skills
-   Add projects
-   View eligible companies
-   Apply for placement drives
-   Track application status
-   View interview schedule
-   Receive notifications
-   View placement history

------------------------------------------------------------------------

## Placement Officer (Admin)

Placement officers can:

-   Manage students
-   Add companies
-   Create placement drives
-   Verify student profiles
-   Check eligibility
-   Schedule interviews
-   Publish results
-   Generate reports
-   View analytics
-   Send notifications

------------------------------------------------------------------------

## Company / HR

Companies can:

-   Register/Login
-   Create recruitment drives
-   Define eligibility criteria
-   View applicants
-   Download resumes
-   Shortlist candidates
-   Schedule interviews
-   Publish final results

------------------------------------------------------------------------

# Core Modules

## Authentication

-   Student Login
-   Company Login
-   Placement Officer Login
-   Forgot Password
-   Email Verification

## Student Profile

Stores:

-   Name
-   Roll Number
-   University
-   Department
-   Semester
-   CGPA
-   Skills
-   Certifications
-   Projects
-   Resume
-   Profile Photo

## Company Management

Stores:

-   Company Name
-   Logo
-   Industry
-   Job Description
-   Salary Package
-   Location
-   Website

## Placement Drives

Each drive contains:

-   Company
-   Eligible Departments
-   Minimum CGPA
-   Backlog Criteria
-   Application Deadline
-   Interview Date

## Eligibility Checker

Automatically validates students based on:

-   University
-   Department
-   CGPA
-   Passing Year
-   Active Backlogs
-   Required Skills

## Job Applications

Application Status:

-   Applied
-   Shortlisted
-   Interview Scheduled
-   Selected
-   Rejected

## Resume Upload

Students upload resumes in PDF format for recruiters to review.

## Interview Scheduling

Includes:

-   Interview Date
-   Time
-   Venue
-   Interview Panel

## Result Management

Displays:

-   Selected Students
-   Waiting List
-   Rejected Candidates

## Notifications

Supports:

-   Drive announcements
-   Interview reminders
-   Result updates
-   Deadline alerts

------------------------------------------------------------------------

# Dashboards

## Student Dashboard

Displays:

-   Profile Completion
-   Applications
-   Upcoming Interviews
-   Selection Status
-   Notifications

## Placement Officer Dashboard

Displays:

-   Total Students
-   Total Companies
-   Placement Percentage
-   Highest Package
-   Average Package
-   Upcoming Drives

## Company Dashboard

Displays:

-   Applications Received
-   Eligible Candidates
-   Shortlisted Candidates
-   Selected Candidates

------------------------------------------------------------------------

# Reports

Generate:

-   Student Reports
-   Company Reports
-   Placement Statistics
-   Department-wise Reports
-   Year-wise Reports
-   Salary Reports

Export Formats:

-   PDF
-   Excel

------------------------------------------------------------------------

# Suggested Database Tables

-   Users
-   Students
-   Companies
-   PlacementDrives
-   Applications
-   Interviews
-   Results
-   Notifications
-   Skills
-   Departments

------------------------------------------------------------------------

# Advanced Features

-   AI Resume Score
-   Skill Recommendation
-   Interactive Charts using Chart.js
-   Email Notifications

------------------------------------------------------------------------

# Django Concepts Used

-   Django Authentication
-   Custom User Model
-   Django ORM
-   ForeignKey Relationships
-   Many-to-Many Relationships
-   Forms
-   File Uploads
-   Django Admin
-   Pagination
-   Search & Filters
-   PDF Generation
-   Excel Export
-   Role-Based Access Control

------------------------------------------------------------------------

# Technology Stack

  Component        Technology
  ---------------- -----------------------------------------------
  Backend          Django 5.x
  Database         PostgreSQL
  Frontend         HTML, CSS, JavaScript
  Charts           Chart.js
  PDF Reports      WeasyPrint / ReportLab
  Excel Export     openpyxl
  Authentication   Django Authentication / Goggle Authentication
  Deployment       Render / Railway / PythonAnywhere

  -----------------------------------------------------------------------
  \# Conclusion

  The Placement Management Portal is a practical, scalable, and
  industry-relevant Django project. It automates the complete campus
  recruitment workflow while demonstrating core software engineering
  concepts such as role-based access control, database management,
  reporting, analytics, and responsive web development. It is well suited
  for a 100-mark college project and can be further enhanced into a
  production-ready application.
  -----------------------------------------------------------------------

# Recommended Django Project Structure

``` text
placement_portal/
│
├── manage.py
├── requirements.txt
├── .env
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/
│   ├── accounts/
│   ├── admin_portal/
│   │   ├── dashboard/
│   │   ├── companies/
│   │   ├── drives/
│   │   ├── reports/
│   │   └── notifications/
│   ├── student_portal/
│   │   ├── dashboard/
│   │   ├── profile/
│   │   ├── resume/
│   │   ├── applications/
│   │   └── interviews/
│   ├── company_portal/
│   │   ├── dashboard/
│   │   ├── profile/
│   │   ├── job_drives/
│   │   ├── applicants/
│   │   └── interviews/
│   ├── common/
│   └── api/
│
├── templates/
│   ├── admin_portal/
│   ├── student_portal/
│   ├── company_portal/
│   └── shared/
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── uploads/
│
├── media/
│   ├── resumes/
│   ├── company_logos/
│   └── profile_photos/
│
└── docs/
    │
    ├── README.md
    │
    ├── 01_SRS.md
    │
    ├── 02_Project_Requirements.md
    │
    ├── 03_Architecture.md
    │
    ├── 04_Rules.md
    │
    ├── 05_Phases.md
    │
    ├── 06_Design.md
    │
    ├── 07_Memory.md
    │
    ├── 08_Database_Design.md
    │
    ├── 09_Testing.md
    │
    └── 10_Deployment.md
```
