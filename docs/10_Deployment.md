# 10_Deployment.md — Deployment Guide

## Placement Management Portal

**Document Version:** 1.0
**Depends on:** `03_Architecture.md` §9–10, `04_Rules.md` §2.1, `09_Testing.md` §9

---

## 1. Purpose

This document covers taking the project from a local Django dev server
to a live, demoable deployment — environment configuration, production
settings changes, and platform-specific steps for the three targets
named in `01_SRS.md` §2.4 (Render, Railway, PythonAnywhere). It also
flags current free-tier limitations on each platform that are easy to
be caught out by close to a submission deadline.

---

## 2. Platform Comparison (checked mid-2026)

| Platform | Postgres included? | Known limitation |
|---|---|---|
| **Render** | Yes — free tier, 1 GB | Free Postgres instances **expire 30 days after creation**; free web services have no persistent disk and spin down after 15 minutes of inactivity (cold start ~30–60s on next request). |
| **Railway** | Yes, via one-time trial credit | Not an ongoing free tier — new accounts get a one-time credit; once it's used, the project bills normally. Fine for a short build-and-demo window, not for a semester-long deployment. |
| **PythonAnywhere** | **Not on new free accounts** | As of the January 2026 plan changes, new free ("Beginner") accounts no longer include database access at all (MySQL moved to the paid Developer tier). Free accounts also can't connect out to an *external* database — outbound access is restricted to an HTTP(S) whitelist, which a Postgres connection doesn't use. A PythonAnywhere free-tier deployment of this project effectively means **falling back to SQLite**, not the documented PostgreSQL stack. |

**Recommendation:** deploy to **Render** as the primary target — it's
the only one of the three that gives you free Postgres matching the
documented stack (`03_Architecture.md` §9) without extra workarounds.
Time the deployment so it's live within the Postgres database's 30-day
window relative to your demo/submission date, and see §12 for how to
avoid losing data if you need it to last longer. Railway is a
reasonable alternative if you still have trial credit. Treat
PythonAnywhere as a SQLite-only fallback unless you're on a paid tier.

---

## 3. Pre-Deployment Checklist

Confirm before deploying (cross-check against `09_Testing.md` §9
sign-off criteria):

- [ ] All Must Pass test cases in `09_Testing.md` pass locally.
- [ ] `DEBUG = False` in production settings.
- [ ] Custom `404.html` / `500.html` templates are in place
      (`04_Rules.md` §5.1).
- [ ] No secrets committed to the repository — `.env` is gitignored.
- [ ] `requirements.txt` is complete and pinned.
- [ ] `ALLOWED_HOSTS` includes the platform's domain.

---

## 4. Environment Variables

Set these on the hosting platform's dashboard (never commit them):

```env
# .env.example — copy real values into the platform's env settings, not into git
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=your-app.onrender.com
DATABASE_URL=postgres://user:password@host:port/dbname
CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com

# Email (for FR-AUTH-03/04, FR-NTF-05)
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-app-password
EMAIL_USE_TLS=True
```

`DATABASE_URL` is provided automatically by Render/Railway when you
attach a Postgres instance — copy it in rather than typing it by hand.

---

## 5. Production Settings Changes

Add to `config/settings.py` (or a separate `settings/production.py` if
you split settings by environment):

```python
import os
import dj_database_url

DEBUG = os.environ.get("DEBUG", "False") == "True"
SECRET_KEY = os.environ["SECRET_KEY"]
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ["DATABASE_URL"],
        conn_max_age=600,
    )
}

# Static files (served via WhiteNoise)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# Security (NFR-02, NFR-04)
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
```

Add to `requirements.txt`:

```text
gunicorn
whitenoise
dj-database-url
psycopg[binary]
python-dotenv
```

---

## 6. Static & Media Files

- **Static files** (CSS/JS): served via WhiteNoise, collected with
  `python manage.py collectstatic` during the build step. No extra
  infrastructure needed.
- **Media files (resumes, logos, profile photos — FR-STU-04/05,
  Company Management fields):** on Render's **free** web service tier,
  there is **no persistent disk** — anything saved to local storage at
  runtime (i.e., a normal Django `FileField`) can be lost whenever the
  service restarts or redeploys. For a short-lived academic demo this
  is often tolerable (re-upload sample files before presenting), but
  if you need uploads to actually persist:
  - Use a free-tier object storage service (e.g., Cloudinary, or AWS
    S3's free tier) with `django-storages`, and point `DEFAULT_FILE_STORAGE`
    at it — this is Stretch-tier polish, not required for MVP
    (`02_Project_Requirements.md` §4).
  - Alternatively, upgrade to a Render paid instance type with a
    persistent disk if the deployment needs to outlive a single demo.

---

## 7. Deploying to Render (primary path)

1. Push the project to a GitHub repository (`main` branch).
2. In the Render dashboard: **New → PostgreSQL** — create a free
   Postgres instance, note its `Internal Database URL`.
3. **New → Web Service** — connect the GitHub repo.
4. **Build Command:**
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   ```
5. **Start Command:**
   ```bash
   gunicorn config.wsgi:application
   ```
6. Add the environment variables from §4 in the service's
   **Environment** tab, using the Postgres instance's connection string
   for `DATABASE_URL`.
7. Deploy. Render assigns a `your-app.onrender.com` URL automatically.
8. Set `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` to that exact domain
   once it's known, and redeploy.

**Reminder:** note the Postgres creation date — plan your demo/
submission before the 30-day free-tier expiry, or export a data dump
beforehand (§12).

---

## 8. Deploying to Railway (alternative)

1. Push to GitHub, then **New Project → Deploy from GitHub repo** in
   Railway.
2. **Add → Database → PostgreSQL** to the project; Railway injects
   `DATABASE_URL` automatically into your service's environment.
3. Add the remaining environment variables from §4 in the service's
   **Variables** tab.
4. Railway auto-detects the Django app; confirm the start command is
   set to `gunicorn config.wsgi:application` under **Settings →
   Deploy**.
5. Trigger a deploy; Railway provides a generated public domain (or
   attach a custom one).
6. Watch your usage against the trial credit — check the Railway
   dashboard's usage/billing page so the project doesn't get
   unexpectedly suspended mid-semester.

---

## 9. Deploying to PythonAnywhere (SQLite fallback only)

Only use this path if Render/Railway aren't options, and accept that
it means running on SQLite rather than the documented PostgreSQL stack
(§2):

1. Upload the project via Git (PythonAnywhere's **Bash console**
   supports `git clone` — GitHub is on the free-tier whitelist).
2. Create a virtualenv and `pip install -r requirements.txt` from the
   Bash console (drop `psycopg`/`dj-database-url` from the production
   requirements list for this path).
3. Set `DATABASES` to the default SQLite config (Django's default) —
   do **not** attempt to point at an external Postgres instance; it
   will not connect on a free account.
4. In the **Web** tab, create a new web app, choose **Manual
   configuration**, and point the WSGI file at
   `config.wsgi.application`.
5. Set the **Static files** mapping in the Web tab (URL `/static/` →
   your `staticfiles` directory) instead of relying on WhiteNoise.
6. Reload the web app from the **Web** tab after any code change
   (PythonAnywhere doesn't auto-deploy from Git pushes).

---

## 10. Database Migration & Seed Data on Production

After first deploy, run (via the platform's shell/console, or as part
of the build command):

```bash
python manage.py migrate
python manage.py createsuperuser   # to log in as an Officer/admin initially
```

Then load the seed data defined in `08_Database_Design.md` §10
(departments, skills, sample students/companies/drives) — either via a
Django data migration, a `loaddata` fixture, or a one-off management
command — so the deployed instance isn't empty for a demo.

---

## 11. Post-Deployment Verification

Run **TC-CRITICAL-01** from `09_Testing.md` §6 against the live URL,
not just locally:

- [ ] Officer can log in and create a company + drive.
- [ ] A seeded eligible student can see and apply to it.
- [ ] Company can view, shortlist, and publish a result.
- [ ] Student sees the updated status and notification.
- [ ] No debug error pages appear anywhere in the flow
      (`DEBUG = False` confirmed).
- [ ] Static assets (CSS/JS/Chart.js output) load correctly over
      HTTPS.

---

## 12. Data Persistence & Backup Notes

Given the free-tier constraints in §2, treat the deployed database as
**demo infrastructure, not permanent storage**:

- Before a Render free Postgres instance's 30-day expiry, either
  upgrade it to a paid instance or export a dump:
  ```bash
  pg_dump $DATABASE_URL > backup.sql
  ```
- Keep your actual source of truth for grading purposes in the Git
  repository and `docs/`, not solely in a database that can expire.
- If the deployment needs to survive past a single demo/viva session,
  budget for at least one paid tier (Render's or a Postgres provider
  like Neon/Supabase's permanent free tier) rather than relying on the
  expiring free database.

---

## 13. Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| 500 error, no detail | `DEBUG=False` hiding the real error | Temporarily check platform logs (Render/Railway dashboard "Logs" tab), not by re-enabling DEBUG in production |
| Static files 404 | `collectstatic` not run, or WhiteNoise misconfigured | Confirm build command includes `collectstatic`; confirm `STATICFILES_STORAGE`/`STORAGES` setting |
| "DisallowedHost" error | `ALLOWED_HOSTS` doesn't match the live domain | Update `ALLOWED_HOSTS` env var to the exact platform domain, redeploy |
| Uploaded resumes disappear after redeploy | No persistent disk on free web service (Render) | Move to object storage per §6, or accept as a known demo limitation |
| Can't connect to database (PythonAnywhere) | Free-tier outbound whitelist blocks external Postgres | Use SQLite per §9 — this is a platform limitation, not a bug |