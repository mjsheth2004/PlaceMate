# 07_Memory.md — Project Memory Log

## Placement Management Portal

**Document Version:** 1.0 (living document — update this regularly)

---

## 1. Purpose

This file is the project's running memory: a short, factual log of what
has actually been completed, when, and why. Its job is to let anyone —
you, a teammate, or an AI assistant with no memory of past
sessions — get back up to speed on real project state in under a
minute, without re-reading every other doc or the whole codebase.

**Update this file every time a meaningful chunk of work finishes** — a
doc completed, a phase milestone hit, a module built, a bug fixed that
took real effort to track down, or a decision made that isn't obvious
from the code alone. If it's not written here, treat it as not having
happened, for planning purposes.

---

## 2. How to Use This Document

- **Newest entries go at the top** of §4 (reverse chronological).
- Keep each entry to a few lines — this is a log, not a report. Link
  out to the relevant doc (`03_Architecture.md`, etc.) for detail
  rather than repeating it here.
- Update §3 (Current Status Snapshot) every time you add a log entry —
  it should always reflect the real, current state, not a past one.
- Don't delete old entries. If something is reversed or redone, add a
  new entry noting the change; the log stays append-only so the
  history is traceable.

### Entry Template

```markdown
### [YYYY-MM-DD] — [Area] — [Short Title]
- What was done:
- Files/docs touched:
- Decisions or notes:
```

---

## 3. Current Status Snapshot

*(Keep this section current — it's the first thing anyone should read.)*

| Area | Status |
|---|---|
| Documentation (`docs/`) | Core docs created. |
| Code implementation | Started. Django project initialized. Login & Registration UI built. |
| Current phase | Phase 1 (Auth & Profile Setup) - UI Implementation |
| Next up | Implement backend authentication logic and database models |

---

## 4. Completed Tasks Log

### 2026-08-01 — Code Implementation — Registration Flow UI Created
- What was done: Built the full UI for User Registration (Role Selection, Student form, Company form). Updated login page with a registration link. Created corresponding views and URLs in the `accounts` app.
- Files/docs touched: `login.html`, `register_selection.html`, `register_student.html`, `register_company.html`, `apps/accounts/views.py`, `apps/accounts/urls.py`.
- Decisions or notes: Forms include CSRF tokens and required fields matching `08_Database_Design.md`. Backend model saving logic to be implemented later.

### 2026-08-01 — Code Implementation — Base UI & Login Page Created
- What was done: Established `base.html` loading Google Fonts (Sora, Inter, JetBrains Mono). Implemented `theme.css` using tokens from `06_Design.md`. Built `login.html` and set it as the default root view.
- Files/docs touched: `theme.css`, `base.html`, `login.html`, `config/urls.py`, `apps/accounts/views.py`, `apps/accounts/urls.py`.
- Decisions or notes: Strictly followed the SaaS-dashboard design aesthetic.

### 2026-08-01 — Documentation — `06_Design.md` created
- What was done: Defined the visual design system — color tokens
  (primary/accent/neutrals/status colors), typography (Sora / Inter /
  JetBrains Mono), component theme tokens, and a ready-to-use
  `theme.css` reference.
- Files/docs touched: `06_Design.md`
- Decisions or notes: Color palette locked to a provided reference
  image. Status badge colors mapped 1:1 onto the `Application.status`
  values from `01_SRS.md` (FR-STU-09). Fixed an accessibility issue in
  the reference (white text on amber "Under Review" badge measured
  ~2.1:1 contrast) by specifying dark text instead.

### 2026-08-01 — Documentation — `05_Phases.md` created
- What was done: Broke the MVP scope into 8 sequential phases mapped
  to an 8-week timeline, each with tasks, FR-ID traceability, and an
  exit condition.
- Files/docs touched: `05_Phases.md`
- Decisions or notes: Phase 5 (Interviews & Results) is the point
  where the MVP Definition of Done (`02_Project_Requirements.md` §3)
  gets met. Eligibility engine (Phase 4) flagged as the highest-risk
  phase for schedule slippage.

### 2026-08-01 — Documentation — `04_Rules.md` created
- What was done: Documented dev conventions, an explicit "avoid" list
  (RBAC-in-templates, unsanitized uploads, bare excepts, etc.), an
  approved-libraries table, error-handling rules, and a dedicated
  section on the boundaries of AI assistance for this project.
- Files/docs touched: `04_Rules.md`
- Decisions or notes: AI assistance is scoped to drafting, scaffolding,
  and review — final scope/architecture calls and anything the student
  needs to defend in a viva remain their own judgment. Real student
  data must never be pasted into an AI tool.

### 2026-08-01 — Documentation — `03_Architecture.md` created
- What was done: Defined the 3-tier system architecture, Django
  app-level breakdown (`accounts`, `admin_portal`, `student_portal`,
  `company_portal`, `common`, `api`), full folder structure, per-role
  app flows, and the technology stack with rationale.
- Files/docs touched: `03_Architecture.md`
- Decisions or notes: Google Authentication (mentioned as optional in
  the original spec) placed in Stretch/Future tier, not MVP, to avoid
  OAuth setup overhead early on.

### 2026-08-01 — Documentation — `02_Project_Requirements.md` created
- What was done: Split all functional requirements from `01_SRS.md`
  into MVP / Stretch / Future tiers, with a concrete MVP Definition of
  Done.
- Files/docs touched: `02_Project_Requirements.md`
- Decisions or notes: Tiering principle — a feature is MVP only if
  removing it breaks the core apply → shortlist → interview → result
  loop.

### 2026-08-01 — Documentation — `01_SRS.md` created
- What was done: Wrote the full Software Requirements Specification —
  functional requirements per module (Auth, Student, Admin, Company,
  Eligibility, Notifications, Reports) with traceable FR IDs, plus
  non-functional requirements, interface requirements, and scope
  boundaries.
- Files/docs touched: `01_SRS.md`
- Decisions or notes: Established the `FR-<MODULE>-<NUMBER>` ID scheme
  used for traceability across every later doc.

---

## 5. Pending / Next Up

- [ ] `08_Database_Design.md` — schema, ER relationships, table
      definitions (referenced but not yet written; `03_Architecture.md`
      §6 assumes this exists).
- [ ] `09_Testing.md` — test plan derived from `01_SRS.md` FR/NFR IDs.
- [ ] `10_Deployment.md` — deployment steps for Render/Railway/
      PythonAnywhere, referenced in `05_Phases.md` Phase 7.
- [ ] Once docs are complete: begin Phase 0 (`05_Phases.md`) — actual
      Django project setup.