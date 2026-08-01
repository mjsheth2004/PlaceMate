# 09_Testing.md — Test Plan

## Placement Management Portal

**Document Version:** 1.0
**Depends on:** `01_SRS.md` (FR/NFR IDs), `02_Project_Requirements.md` (tiers), `05_Phases.md` (Phase 7)

---

## 1. Purpose

This document defines how the system gets tested against the
requirements in `01_SRS.md`. Every test case (`TC-...`) maps to a
requirement ID (`FR-...`/`NFR-...`), so coverage is checkable at a
glance rather than assumed. This is executed primarily in Phase 7
(`05_Phases.md`), but individual test cases should be run as each
module is built, not saved up entirely for the end.

---

## 2. Testing Approach

| Level | Tool | What it covers |
|---|---|---|
| Unit tests | Django's `TestCase` (or `pytest-django`) | Model validation, eligibility service logic, form validation |
| Integration tests | Django's `TestCase` + test client | View-level behavior: RBAC, application flow, status transitions |
| Manual / UI tests | Browser, using the checklist in §5–§7 | End-to-end flows, visual/UX checks, file upload behavior |
| Regression | Re-run full suite | Before each phase sign-off and before final deployment |

**Test database:** Django's test runner creates and tears down a
separate PostgreSQL test database automatically — never test against
data that matters.

**Seed/fixture data:** use the seed data defined in
`08_Database_Design.md` §10 (departments, skills, sample students/
companies/drives spanning different eligibility combinations) so
eligibility and RBAC tests have real edge cases to exercise, not just
happy-path data.

---

## 3. Priority Key

- **Must Pass (M):** blocks the MVP Definition of Done
  (`02_Project_Requirements.md` §3) if failing.
- **Should Pass (S):** Stretch-tier feature; failing is a known gap,
  not a blocker.

---

## 4. Test Cases by Module

### 4.1 Authentication (`TC-AUTH`)

| TC ID | Verifies | Steps | Expected Result | Priority |
|---|---|---|---|---|
| TC-AUTH-01 | FR-AUTH-01 | Register as Student, Company, and Officer with valid data | Account created for each role; redirected appropriately | M |
| TC-AUTH-02 | FR-AUTH-02 | Log in with correct email/password | Redirected to the correct role-specific dashboard | M |
| TC-AUTH-02b | FR-AUTH-02 | Log in with incorrect password | Login rejected with a clear error, no session created | M |
| TC-AUTH-03 | FR-AUTH-03 | Register, then click the emailed verification link | `email_verified` becomes `True`; full access granted | S |
| TC-AUTH-04 | FR-AUTH-04 | Request password reset, follow link, set new password | Login succeeds with new password; old password no longer works | M |
| TC-AUTH-05 | FR-AUTH-05 | While logged in as Student, directly navigate to an Officer-only URL | Access denied (redirect or 403), not the Officer view | M |
| TC-AUTH-06 | FR-AUTH-06 | Leave a session idle past the configured timeout, then act | User is logged out and must log in again | S |

### 4.2 Student Module (`TC-STU`)

| TC ID | Verifies | Steps | Expected Result | Priority |
|---|---|---|---|---|
| TC-STU-01 | FR-STU-01 | Create/edit profile with name, roll no., university, department, semester, CGPA | Data saves and persists on reload | M |
| TC-STU-02 | FR-STU-02 | Add and remove skills and projects | Changes reflected immediately and on reload | M |
| TC-STU-03 | FR-STU-03 | Add a certification | Certification appears on profile | S |
| TC-STU-04 | FR-STU-04 | Upload a resume as PDF; then attempt to upload a `.exe` file | Valid PDF accepted; invalid file type rejected server-side | M |
| TC-STU-04b | FR-STU-04 / NFR-03 | Upload a resume exceeding the max file size | Upload rejected with a clear error | M |
| TC-STU-05 | FR-STU-05 | Upload a profile photo (JPEG/PNG) | Accepted and displayed on profile | S |
| TC-STU-06 | FR-STU-06 | Fill profile partially, then fully | Completion percentage increases and reaches 100% when complete | S |
| TC-STU-07 | FR-STU-07 | Log in as a student meeting a drive's criteria | Drive appears in "eligible drives" list | M |
| TC-STU-07b | FR-STU-07 | Log in as a student **not** meeting a drive's criteria | Drive does **not** appear in the eligible list | M |
| TC-STU-08 | FR-STU-08 | Apply to an eligible drive | Application created with status `Applied` | M |
| TC-STU-09 | FR-STU-09 | Officer/Company changes an application's status | Student's status view updates to match | M |
| TC-STU-10 | FR-STU-10 | After an interview is scheduled for the student's application | Interview date/time/venue/panel visible to the student | M |
| TC-STU-11 | FR-STU-11 | A drive is announced / a result is published | Student receives a corresponding notification | M |
| TC-STU-12 | FR-STU-12 | Student is marked `Selected` on a drive | Drive appears in the student's placement history | S |

### 4.3 Placement Officer / Admin Module (`TC-ADM`)

| TC ID | Verifies | Steps | Expected Result | Priority |
|---|---|---|---|---|
| TC-ADM-01 | FR-ADM-01 | Officer views and verifies a student profile | `is_verified` updates; visible in student list | M |
| TC-ADM-02 | FR-ADM-02 | Officer adds, edits, and removes a company record | Changes persist and reflect in company list | M |
| TC-ADM-03 | FR-ADM-03 | Officer creates/approves a placement drive | Drive status moves to `published`; visible to eligible students | M |
| TC-ADM-04 | FR-ADM-04 | Officer sets/overrides eligibility criteria on a drive | Criteria save; eligibility results change accordingly | M |
| TC-ADM-05 | FR-ADM-05 | Officer views auto-flagged eligible students for a drive | List matches the eligibility service's own output (cross-check against TC-ELG-*) | M |
| TC-ADM-06 | FR-ADM-06 | Officer schedules/modifies an interview slot | Interview record created/updated; visible to student and company | M |
| TC-ADM-07 | FR-ADM-07 | Officer publishes final results for a drive | Application statuses update to `Selected`/`Rejected`; notifications fire (TC-NTF-03) | M |
| TC-ADM-08 | FR-ADM-08 | Officer generates a PDF and an Excel report | Both files download and open correctly with expected data | M |
| TC-ADM-09 | FR-ADM-09 | Officer views dashboard analytics | Totals, placement %, highest/average package match underlying data | M |
| TC-ADM-10 | FR-ADM-10 | Officer sends a manual notification | Recipients see it in their notification list | S |

### 4.4 Company / HR Module (`TC-CMP`)

| TC ID | Verifies | Steps | Expected Result | Priority |
|---|---|---|---|---|
| TC-CMP-01 | FR-CMP-01 | Register and log in as a company | Company dashboard accessible after login | M |
| TC-CMP-02 | FR-CMP-02 | Create a drive with job description, salary, location, eligibility | Drive record created, pending or published per approval flow | M |
| TC-CMP-03 | FR-CMP-03 | View applicant list for a drive | All applications for that drive are listed, none from other drives | M |
| TC-CMP-04 | FR-CMP-04 | Download an applicant's resume | Correct file downloads for the correct applicant | M |
| TC-CMP-05 | FR-CMP-05 | Shortlist a candidate | Application status changes to `Shortlisted` | M |
| TC-CMP-06 | FR-CMP-06 | Confirm an interview schedule | Interview record reflects company-confirmed details | M |
| TC-CMP-07 | FR-CMP-07 | Publish final results for the drive | Statuses update; students notified | M |
| TC-CMP-08 | FR-CMP-08 | View company dashboard summary | Counts (applied/eligible/shortlisted/selected) match underlying data | S |

### 4.5 Eligibility Checker (`TC-ELG`)

This module gets the most negative/edge-case testing — it's flagged in
`05_Phases.md` §6 as the highest-risk area for bugs.

| TC ID | Verifies | Steps | Expected Result | Priority |
|---|---|---|---|---|
| TC-ELG-01 | FR-ELG-01 | Student CGPA exactly at, just above, and just below a drive's `min_cgpa` | At/above → eligible; below → ineligible (boundary tested precisely) | M |
| TC-ELG-02 | FR-ELG-02 | Student in an eligible vs. non-eligible department | Correctly included/excluded | M |
| TC-ELG-03 | FR-ELG-03 | Student passing year matches vs. doesn't match drive's requirement | Correctly included/excluded | M |
| TC-ELG-04 | FR-ELG-04 | Student backlog count at, above, and below `max_backlogs` | At/below → eligible; above → ineligible | M |
| TC-ELG-05 | FR-ELG-05 | Student with vs. without a drive's required skill(s) | Correctly included/excluded when skill filter is set | S |
| TC-ELG-06 | FR-ELG-06 | An ineligible student attempts to `POST` an apply request directly (bypassing the UI) | Application rejected server-side, not just hidden client-side | M |

### 4.6 Notifications (`TC-NTF`)

| TC ID | Verifies | Steps | Expected Result | Priority |
|---|---|---|---|---|
| TC-NTF-01 | FR-NTF-01 | Officer publishes a new drive | Eligible students receive a "drive announced" notification | M |
| TC-NTF-02 | FR-NTF-02 | An interview's scheduled time approaches | Applicant receives a reminder notification | S |
| TC-NTF-03 | FR-NTF-03 | A result is published | Applicant receives a "result published" notification | M |
| TC-NTF-04 | FR-NTF-04 | A drive's deadline approaches, student hasn't applied | Eligible, non-applied students receive a deadline alert | S |
| TC-NTF-05 | FR-NTF-05 | Notification triggers with email channel enabled | Notification appears in-app and via email | S |

### 4.7 Reports (`TC-RPT`)

| TC ID | Verifies | Steps | Expected Result | Priority |
|---|---|---|---|---|
| TC-RPT-01 | FR-RPT-01 | Generate a student report | Report reflects that student's actual profile + application history | M |
| TC-RPT-02 | FR-RPT-02 | Generate a company-wise report | Matches that company's actual drives and outcomes | S |
| TC-RPT-03 | FR-RPT-03 | Generate department-wise / year-wise statistics | Numbers match a manual count against seed data | M |
| TC-RPT-04 | FR-RPT-04 | Generate a salary/package report | Figures match selected students' recorded packages | S |
| TC-RPT-05 | FR-RPT-05 | Export any report as both PDF and Excel | Both formats download, open, and contain matching data | M |

---

## 5. Non-Functional Requirement Testing

| NFR ID | Test Approach | Expected Result |
|---|---|---|
| NFR-01 (Performance) | Load a dashboard/drive-listing page with seed data loaded; time it | Loads within ~2–3 seconds under normal single-institution load |
| NFR-02 (Security) | Inspect the `User` table directly in the DB | Passwords are hashed, never stored in plaintext |
| NFR-03 (Security) | Attempt to upload a disguised file (e.g., a `.exe` renamed to `.pdf`) | Rejected by server-side content-type validation, not just extension |
| NFR-04 (Security) | Attempt to access another role's or another user's data via direct URL/ID manipulation | Denied at the view/permission level in every case |
| NFR-05 (Usability) | Time a full "apply to a drive" flow from dashboard | Completable within 3 clicks from the dashboard |
| NFR-06 (Reliability) | Submit invalid form data (blank required fields, malformed CGPA, etc.) | Clear validation message shown; no stack trace exposed |
| NFR-07 (Maintainability) | Code review against `03_Architecture.md` app structure | Logic lives in the correct app/module, not scattered |
| NFR-08 (Scalability) | Load a list view with 100+ seeded records | Pagination active; page remains responsive |
| NFR-09 (Portability) | Deploy to the chosen platform (Render/Railway/PythonAnywhere) using only `.env` config changes | Deploys without code changes |
| NFR-10 (Auditability) | Change an application's status, then inspect the record | `updated_at` timestamp reflects the change |

---

## 6. Critical Path Test — Full Recruitment Loop

This single scenario test is the highest-value test in the suite: it
directly verifies the MVP Definition of Done from
`02_Project_Requirements.md` §3.

**TC-CRITICAL-01:**
1. Officer adds a company and creates a drive with defined eligibility.
2. A seeded eligible student logs in, sees the drive, and applies.
3. Company views the applicant, downloads the resume, and shortlists.
4. Officer/Company schedules an interview; student sees it.
5. Officer/Company publishes the result as `Selected`.
6. Student sees the updated status, a notification, and the drive
   appears in their placement history.

**Expected Result:** every step completes through the UI alone, with
no manual database edits at any point. This test should be run at the
end of Phase 5 (per `05_Phases.md`) and again before final deployment.

---

## 7. Manual UI / UX Checklist

- [ ] All three dashboards (Student, Company, Officer) render correctly
      on both desktop and a mobile-width viewport.
- [ ] Status badges use the correct colors/labels per `06_Design.md` §3.3.
- [ ] Form validation errors display inline, not as raw exceptions.
- [ ] Custom 404 and 500 pages display instead of Django's debug pages
      (with `DEBUG = False`).
- [ ] Navigation is role-appropriate — no broken links to another
      role's views.
- [ ] Charts (Chart.js) on dashboards render with real seed data, not
      placeholder/empty states, once data exists.

---

## 8. Bug Tracking

For a project of this size, a simple running list is sufficient —
either a `docs/BUGS.md` file or issues in your Git host. Each entry
should note: which `TC-` or `FR-` ID it relates to, steps to
reproduce, and status (open/fixed/won't-fix with reason). Log entries
for significant fixes in `07_Memory.md` per its own update rules.

---

## 9. Sign-Off Criteria

The project is ready to move into Phase 7's deployment step
(`05_Phases.md`) when:

- [ ] All **Must Pass (M)** test cases in §4 pass.
- [ ] All **NFR** checks in §5 pass.
- [ ] **TC-CRITICAL-01** (§6) passes end-to-end without manual
      intervention.
- [ ] Any failing **Should Pass (S)** test case is either fixed or
      explicitly logged as a known gap (not silently skipped).