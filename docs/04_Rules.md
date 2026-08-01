# 04_Rules.md — Development Rules & Boundaries

## Placement Management Portal

**Document Version:** 1.0
**Depends on:** `01_SRS.md`, `02_Project_Requirements.md`, `03_Architecture.md`

---

## 1. Purpose

This document sets the ground rules for building the project
consistently — what to do, what to avoid, which libraries are approved,
how errors should be handled, and where AI assistance (e.g., Claude)
is and isn't appropriate. It exists so that decisions made once don't
have to be re-litigated mid-build, and so the final submission reflects
consistent, defensible engineering choices.

---

## 2. What To Do

### 2.1 Django & Coding Conventions

- Follow Django's app-per-domain structure defined in
  `03_Architecture.md` — don't put unrelated logic in `common` just
  because it's convenient.
- Keep business logic (eligibility checks, report assembly,
  notification triggers) in **service functions/modules**, not
  scattered across views — views should stay thin (fetch, call
  service, render).
- Use Django's **ORM** for all database access; no raw SQL unless a
  specific query genuinely can't be expressed via the ORM (and if so,
  document why in a code comment).
- Use **Django Forms/ModelForms** for all user input — never trust
  client-side validation alone (ties to NFR-03/NFR-04 in `01_SRS.md`).
- Name things after the domain, not the implementation: `Application`,
  `PlacementDrive`, `EligibilityService` — not `Data1`, `Helper`,
  `Utils2`.
- Every model should have `created_at`/`updated_at` timestamps (via a
  shared abstract base model in `apps/common`) to support NFR-10
  (auditability).
- Write a docstring or comment for any non-obvious eligibility, RBAC,
  or report-generation logic — this is the code most likely to be
  questioned in a viva/demo.
- Commit early, commit often, with descriptive messages tied to a
  feature or FR ID where possible (e.g., `feat: implement FR-STU-08
  apply to drive`).

### 2.2 Git & Version Control

- One feature/module per branch where feasible; merge into `main` (or
  `dev`) only once it runs without errors.
- Never commit `.env`, `media/`, or any file containing real student
  data, resumes, or credentials.
- Tag or note the commit that represents "MVP complete" per the
  Definition of Done in `02_Project_Requirements.md` §3 — useful for
  both grading and personal tracking.

### 2.3 Documentation Discipline

- If a requirement changes, update `01_SRS.md`/`02_Project_Requirements.md`
  first, then the code — not the other way around.
- Keep `08_Database_Design.md` in sync with actual model definitions;
  a schema doc that doesn't match the code is worse than no doc.

---

## 3. What To Avoid

- **Don't** put authentication or eligibility logic directly in
  templates (e.g., `{% if user.cgpa > 7 %}`) — this bypasses
  server-side enforcement (NFR-04) and is not a substitute for a real
  permission check.
- **Don't** hardcode eligibility values (CGPA thresholds, backlog
  limits) in view code — they belong on the `PlacementDrive` model so
  officers/companies can configure them per drive (FR-ADM-04).
- **Don't** store uploaded resumes or photos with unsanitized original
  filenames — this risks path traversal and filename collisions; use
  Django's storage system to generate safe paths.
- **Don't** trust file uploads by extension alone — validate MIME
  type/content server-side (NFR-03), not just `.pdf`/`.jpg` suffix
  matching.
- **Don't** expose Django's debug error pages or stack traces in
  anything resembling a production/demo build — set `DEBUG = False`
  and configure custom error pages before deployment.
- **Don't** let any role query or view data outside its own scope by
  manipulating a URL/ID (e.g., a student viewing another student's
  resume by guessing a URL) — every object-level view must check
  ownership/permission, not just login status.
- **Don't** add a new third-party library "just to try it" mid-build
  without checking it against §4 — every new dependency adds risk and
  setup overhead close to a deadline.
- **Don't** silently swallow exceptions (bare `except:` blocks) —
  this hides bugs that will surface unpredictably during a live demo.

---

## 4. Approved Libraries & Dependencies

These match the stack defined in `03_Architecture.md` §9 and are
pre-approved for use without further discussion:

| Purpose | Library |
|---|---|
| Web framework | Django 5.x |
| Database driver | `psycopg` (PostgreSQL) |
| PDF generation | WeasyPrint or ReportLab |
| Excel export | `openpyxl` |
| Charts | Chart.js (via CDN or static bundle) |
| Environment config | `python-dotenv` or `django-environ` |
| Forms/validation | Django built-in forms |

### Adding a New Dependency

Before adding anything not on this list:
1. Check it's actively maintained and has reasonable documentation.
2. Confirm it doesn't duplicate something Django or an approved
   library already does.
3. Add it to `requirements.txt` with a pinned version, and note *why*
   it was added in the commit message.
4. If it changes the tech stack meaningfully, update
   `03_Architecture.md` §9 to keep the docs accurate.

Avoid adding heavy dependencies (e.g., a separate task queue like
Celery, or a frontend framework like React) unless a Stretch/Future
feature genuinely requires it — most of MVP does not.

---

## 5. Error Handling Guidelines

### 5.1 User-Facing Errors

- Form validation errors should render inline, next to the relevant
  field, using Django's standard form error rendering — never a raw
  exception message.
- Use Django's `messages` framework for action confirmations and
  non-field errors (e.g., "You are not eligible for this drive").
- Custom `404.html` and `500.html` templates should be in place before
  deployment (`templates/shared/`), so a broken link or server error
  never shows a raw traceback to a student, company, or evaluator.

### 5.2 Server-Side Handling & Logging

- Wrap external operations that can legitimately fail (file uploads,
  PDF/Excel generation, email sending) in explicit `try/except` blocks
  with a specific exception type — not a bare `except:`.
- Log unexpected errors (via Python's `logging` module) rather than
  printing to console — this matters even for a student project if
  you want to debug issues after a demo.
- Never log sensitive data (passwords, full resumes, raw CGPA lists)
  at a verbosity level that could end up in a shared log file.

### 5.3 Validation Rules

- Validate at the **model** level (via `clean()`/validators) wherever
  a rule is fundamental to data integrity (e.g., CGPA must be between
  0 and 10) — not only in the form.
- Re-validate eligibility server-side at the moment of applying
  (FR-ELG-06), even though the student only sees eligible drives in
  the UI — the UI list is a convenience, not a security boundary.

---

## 6. Boundaries of AI Assistance

This project is being built with AI assistance (e.g., Claude) for
planning, documentation, and code generation. The following boundaries
keep that assistance useful without undermining the learning goals of
the project or the integrity of the submission.

### 6.1 What AI Assistance Is Appropriate For

- Drafting and refining documentation (SRS, architecture, this file).
- Scaffolding boilerplate (models, forms, views, templates) that you
  then read, understand, and adapt.
- Explaining Django concepts, debugging error messages, and reviewing
  code for issues.
- Generating test cases and sample/seed data.
- Suggesting report/query structures and eligibility logic — checked
  against actual requirements before use.

### 6.2 What Requires Your Own Judgment

- **Final scope decisions** — what's MVP vs. Stretch vs. Future is
  documented in `02_Project_Requirements.md`; AI can suggest tiering,
  but you decide and own the final call, especially before a
  submission deadline.
- **Architecture trade-offs** — AI can lay out options, but which
  approach fits your timeline, grading rubric, and skill level is your
  decision.
- **Anything you'll be asked to explain in a viva/demo** — if you
  can't explain why a piece of code works, don't submit it as-is;
  understand it first, even if AI wrote the first draft.
- **Grading-sensitive originality** — check your institution's
  academic integrity policy on AI-assisted work; where required,
  disclose AI assistance appropriately.

### 6.3 Data & Privacy Rules When Using AI Tools

- **Never paste real student data** (actual names, roll numbers,
  CGPA, resumes, contact info) into an AI chat tool — use synthetic/
  seed data for any example, question, or debugging session.
- Treat any `.env`, API keys, or database credentials as strictly
  off-limits to share with AI tools, in code snippets or otherwise.
- If asking AI to review real code, confirm it doesn't contain
  hardcoded secrets first.

### 6.4 Trust, But Verify

- AI-generated code and documentation should be **reviewed, run, and
  tested** — not copy-pasted blindly. This is especially true for
  eligibility logic, authentication/RBAC code, and anything touching
  file uploads, where subtle mistakes have real consequences.
- If AI-generated content conflicts with an already-agreed
  requirement in `01_SRS.md` or `02_Project_Requirements.md`, the
  documented requirement wins — flag the conflict and resolve it
  deliberately, don't let generated code silently drift from spec.

---

## 7. Review Checklist (Before Any Merge/Demo)

- [ ] No hardcoded secrets, credentials, or real student data in the
      repo.
- [ ] All new views enforce RBAC (role check + object-level ownership
      where relevant).
- [ ] All file uploads validate type and size server-side.
- [ ] No bare `except:` blocks; errors are logged, not silently
      dropped.
- [ ] `DEBUG = False` and custom error pages are in place before any
      public deployment.
- [ ] New dependencies are in `requirements.txt` and reflected in
      `03_Architecture.md` if they change the stack.
- [ ] Relevant docs (`01_SRS.md`, `02_Project_Requirements.md`,
      `08_Database_Design.md`) are updated if the change affects them.