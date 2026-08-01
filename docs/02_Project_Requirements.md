# 02_Project_Requirements.md — Project Requirements & Scope

## Placement Management Portal

**Document Version:** 1.0
**Depends on:** `01_SRS.md` (full functional requirement definitions and IDs)

---

## 1. Purpose

`01_SRS.md` defines *what* every requirement is. This document defines
*which of those requirements get built, and in what order*, given a
single-semester/hackathon academic timeline. Requirements are grouped
into three tiers:

- **MVP** — Must exist for the project to function and be demoable/gradable.
- **Stretch** — Should be added if MVP is complete with time remaining.
- **Future Enhancements** — Could be built post-submission; not required
  to demonstrate core competency for this project.

Detailed week-by-week scheduling of the MVP tier lives in `05_Phases.md`.
This document only defines *what* belongs in each tier and *why*.

---

## 2. Scope Tiering Principle

A feature is placed in MVP only if removing it would break the core
recruitment loop: **a student can register, get matched to an eligible
drive, apply, get shortlisted/interviewed, and see a result — with an
Officer and a Company able to manage that loop end-to-end.** Everything
that enhances, polishes, or extends that loop — without which the loop
still works — is Stretch or Future.

---

## 3. MVP — Must-Have (Tier 1)

These map directly to **M**-priority items in `01_SRS.md` §3.

### 3.1 Authentication
- FR-AUTH-01 — Role-based registration (Student / Company / Officer)
- FR-AUTH-02 — Login for all roles
- FR-AUTH-04 — Forgot password flow
- FR-AUTH-05 — Role-based access control enforced on all views

### 3.2 Student
- FR-STU-01 — Profile creation/editing
- FR-STU-02 — Skills and projects
- FR-STU-04 — Resume upload (PDF)
- FR-STU-07 — View eligible drives
- FR-STU-08 — Apply to a drive
- FR-STU-09 — Track application status
- FR-STU-10 — View interview schedule
- FR-STU-11 — Receive core notifications (drive + result)

### 3.3 Placement Officer / Admin
- FR-ADM-01 — Manage/verify student profiles
- FR-ADM-02 — Manage companies
- FR-ADM-03 — Create placement drives
- FR-ADM-04 — Define eligibility criteria
- FR-ADM-05 — Automated eligibility flagging
- FR-ADM-06 — Schedule interviews
- FR-ADM-07 — Publish results
- FR-ADM-08 — Generate core reports (PDF/Excel)
- FR-ADM-09 — Dashboard analytics (totals, %, packages)

### 3.4 Company / HR
- FR-CMP-01 — Register/login
- FR-CMP-02 — Create a drive with eligibility criteria
- FR-CMP-03 — View applicants
- FR-CMP-04 — Download resumes
- FR-CMP-05 — Shortlist candidates
- FR-CMP-06 — Confirm interview schedule
- FR-CMP-07 — Publish results

### 3.5 Eligibility Checker
- FR-ELG-01 — CGPA validation
- FR-ELG-02 — Department validation
- FR-ELG-03 — Passing year validation
- FR-ELG-04 — Backlog validation
- FR-ELG-06 — Block ineligible applications at view level

### 3.6 Notifications
- FR-NTF-01 — Drive announcement
- FR-NTF-03 — Result published

### 3.7 Reports
- FR-RPT-01 — Student report
- FR-RPT-05 — PDF/Excel export (basic — student and drive reports only)

### MVP Definition of Done
The system is MVP-complete when: a seeded Officer can add a company and
drive; a seeded Student who meets the criteria can see and apply to it;
the Company can view, shortlist, and publish a result for that
applicant; and the Student sees the updated status and a notification —
all without manual database edits.

---

## 4. Stretch Goals — Should-Have (Tier 2)

Build these only after the MVP Definition of Done (§3) is met and
verified. Maps to **S**-priority items in `01_SRS.md` §3.

| Area | Feature | SRS ID |
|---|---|---|
| Auth | Email verification before full access | FR-AUTH-03 |
| Auth | Auto logout after inactivity | FR-AUTH-06 |
| Student | Certifications field | FR-STU-03 |
| Student | Profile-completion percentage indicator | FR-STU-06 |
| Student | Placement history view | FR-STU-12 |
| Admin | Manual/ad-hoc notifications to students | FR-ADM-10 |
| Company | Company dashboard summary (applied/eligible/shortlisted/selected counts) | FR-CMP-08 |
| Eligibility | Required-skills matching | FR-ELG-05 |
| Notifications | Interview reminders | FR-NTF-02 |
| Notifications | Deadline alerts | FR-NTF-04 |
| Notifications | Optional email delivery channel | FR-NTF-05 |
| Reports | Department-wise and year-wise statistics | FR-RPT-03 |
| Reports | Company-wise report | FR-RPT-02 |
| Reports | Salary/package report | FR-RPT-04 |

**Rationale:** these features materially improve usability and
completeness (and will strengthen a project demo/viva), but the core
recruitment loop functions correctly without them.

---

## 5. Future Enhancements — Could-Have (Tier 3)

Not scheduled in `05_Phases.md`. Documented here so they aren't lost,
and so the architecture (`03_Architecture.md`) doesn't accidentally
foreclose them.

| Feature | Notes |
|---|---|
| AI Resume Score | Would need an ML/NLP scoring approach or a third-party API; out of scope for the core Django build. |
| Skill Recommendation Engine | Suggests skills to students based on drives they're ineligible for; needs a recommendation heuristic or model. |
| Advanced Interactive Analytics | Deeper Chart.js dashboards (trend lines, cohort comparisons) beyond the MVP's basic totals. |
| Real-time Chat (Student ↔ Recruiter) | Would require WebSockets/Django Channels; explicitly out of scope per `01_SRS.md` §6.3. |
| Native Mobile App | Web-responsive only for this project; out of scope per `01_SRS.md` §6.3. |
| ERP Integration | Auto-import of student academic records from a college ERP instead of manual entry. |
| Payment Processing | Not required — the platform does not collect fees. Out of scope per `01_SRS.md` §6.3. |

---

## 6. Non-Functional Requirements

All NFRs (performance, security, usability, reliability, scalability,
portability, auditability) defined in `01_SRS.md` §5 apply across all
tiers — they are not deferred to Stretch or Future. Security-related
items in particular (NFR-02, NFR-03, NFR-04) must be respected even in
the MVP build.

---

## 7. Out of Scope (Reaffirmed)

Per `01_SRS.md` §6.3, the following are not part of this project at any
tier unless explicitly revisited:

- Payment processing
- Native mobile applications
- Real-time chat

---

## 8. Change Control

If a feature needs to move between tiers (e.g., a Stretch item becomes
necessary for the demo), update this document first, then reflect the
change in `05_Phases.md`'s week-by-week plan. Keep SRS IDs (`01_SRS.md`)
as the single source of truth for requirement wording — this document
only reorders priority, it does not redefine requirements.