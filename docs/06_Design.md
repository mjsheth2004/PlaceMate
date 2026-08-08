# 06_Design.md — Visual Design System

## Placement Management Portal

**Document Version:** 1.0
**Depends on:** `03_Architecture.md` (frontend stack: HTML/CSS/JS templates)

---

## 1. Purpose

This document defines the visual design system — color, theme, and
typography — for the portal, so every screen across the Student,
Company, and Officer dashboards looks and feels like one product
rather than three disconnected UIs. Color values below are locked to
the palette reference already agreed on; typography is specified to
complement it.

---

## 2. Design Direction

The product's job is to make a formal, high-stakes process (recruitment
outcomes) feel clear and trustworthy on screen — not playful, not
decorative. The palette is a clean, structured SaaS-dashboard direction:
deep teal as the primary brand color, warm gold as the supporting accent, a terracotta highlight, and a soft cream background. Status
colors carry real information (where an application stands), so they're
treated as functional, not decorative.

Typography follows the same logic: a distinct but restrained geometric
display face for headings (so the product has a identity beyond "default
system font"), paired with a highly legible body face built for
data-dense screens, plus a monospace face reserved specifically for
numeric records (CGPA, roll numbers, packages) so those figures read as
verified data, not prose.

---

## 3. Color System

### 3.1 Primary & Accent

| Token | Hex | RGB | Usage |
|---|---|---|---|
| `--color-primary` | `#2A9D8F` | 37, 99, 235 | Headers, navigation, primary buttons, links |
| `--color-accent` | `#2A9D8F` | 13, 148, 136 | Apply buttons, success states, highlights |

### 3.2 Neutrals & Layout

| Token | Hex | Usage |
|---|---|---|
| `--color-background` | `#FDFBF7` | Overall page background |
| `--color-surface` | `#FDFBF7` | Cards, modals, forms |
| `--color-text-primary` | `#264653` | Main headings, body text |
| `--color-text-secondary` | `#8A6D3B` | Captions, labels, secondary text |
| `--color-border` | `#E9C46A` | Dividers, input outlines |

### 3.3 Status Colors — Application Tracking

These map directly to the application status values defined in
`01_SRS.md` (FR-STU-09). Use this table as the single source of truth
when implementing the `Application.status` choices and their badge
colors:

| Design Label | SRS Status (FR-STU-09) | Hex | Token |
|---|---|---|---|
| Applied | Applied | `#2A9D8F` | `--status-applied` |
| Under Review | Shortlisted | `#E9C46A` | `--status-shortlisted` |
| Interview | Interview Scheduled | `#E76F51` | `--status-interview` |
| Hired | Selected | `#2A9D8F` | `--status-selected` |
| Rejected | Rejected | `#E76F51` | `--status-rejected` |

Use the **Design Label** as the on-screen badge text (it reads better
to students/companies) while the **SRS Status** stays as the backend
enum value — keep a single mapping constant in code so the two never
drift apart.

### 3.4 Accessibility Notes on Color

- **"Under Review" badge:** white text on `#E9C46A` measures roughly
  **2.1:1 contrast** — well below the 4.5:1 needed for body-sized text
  under WCAG AA. Use dark text on this badge instead
  (`--color-text-primary` `#264653`, which gives ~8.3:1), not white.
- **Other status badges** (`#2A9D8F`, `#E76F51`, `#E76F51`, `#2A9D8F`)
  with white text land in the 2.5–3.7:1 range — fine for large/bold
  labels or icon-only chips, but borderline-to-failing for small badge
  text at AA. Before locking the UI, run each pairing through a
  contrast checker; if small white-on-color text is important for
  visual consistency, use the `-600`/`-700` shade of each hue (e.g.,
  `#2A9D8F` instead of `#2A9D8F` for the Applied badge — conveniently
  the same as `--color-primary`) rather than the base shade shown above.
- `--color-text-secondary` (`#8A6D3B`) on `--color-background` /
  `--color-surface` sits well above the AA minimum — ensuring good contrast
  for labels and captions.

---

## 4. Typography

### 4.1 Type Families

| Role | Typeface | Fallback Stack |
|---|---|---|
| Display / Headings | **Sora** | `'Sora', 'Segoe UI', system-ui, sans-serif` |
| Body / UI | **Inter** | `'Inter', 'Segoe UI', system-ui, sans-serif` |
| Numeric / Data | **JetBrains Mono** | `'JetBrains Mono', 'Consolas', monospace` |

**Why this pairing:** Sora's geometric, slightly rounded letterforms
give the product a distinct identity for headings without tipping into
anything decorative — appropriate for a formal recruitment tool. Inter
is purpose-built for dense UI text and pairs cleanly with Sora since
both are neo-grotesque-adjacent without being identical. JetBrains Mono
is reserved narrowly: CGPA, roll numbers, salary packages, and IDs are
set in it so verified figures are visually distinguishable from
ordinary prose at a glance — useful on a screen where a CGPA cutoff or
a package number is often the single fact someone is scanning for.

Both Sora and Inter are free, self-hostable, and available via Google
Fonts — no licensing concerns for an academic project.

### 4.2 Type Scale

| Role | Font | Size | Weight | Line Height | Letter Spacing | Usage |
|---|---|---|---|---|---|---|
| H1 | Sora | 2.5rem (40px) | 700 Bold | 1.2 | -0.01em | Page titles ("Placement Drives", dashboard titles) |
| H2 | Sora | 2rem (32px) | 600 SemiBold | 1.25 | -0.01em | Section headers |
| H3 | Sora | 1.5rem (24px) | 600 SemiBold | 1.3 | normal | Card / module titles (e.g., drive card headline) |
| H4 | Sora | 1.25rem (20px) | 500 Medium | 1.35 | normal | Sub-section headers, modal titles |
| Body Large | Inter | 1.125rem (18px) | 400 Regular | 1.6 | normal | Intro text, empty-state messaging |
| Body | Inter | 1rem (16px) | 400 Regular | 1.6 | normal | Default paragraph, form labels' descriptions |
| Body Small | Inter | 0.875rem (14px) | 400 Regular | 1.5 | normal | Helper text, table cell text |
| Caption / Label | Inter | 0.75rem (12px) | 500 Medium | 1.4 | 0.04em (uppercase) | Field labels, table headers, status badge text |
| Data / Numeric | JetBrains Mono | 0.875–1rem | 500 Medium | 1.4 | normal | CGPA, roll numbers, packages, drive IDs |

### 4.3 Weight Usage Rules

- Never use Sora below 500 (Medium) — its lighter weights read as too
  thin for headings at this scale.
- Never use Inter above 600 (SemiBold) for body copy — reserve Bold
  (700) for the rare case of an inline emphasis, not entire labels.
- Buttons use Inter SemiBold (600), not Sora — buttons are actions, not
  headings, and should read as UI, not display type.

### 4.4 Numeric & Tabular Data Formatting

- CGPA, roll numbers, drive package/salary figures, and any generated
  ID (student ID, drive ID) are set in **JetBrains Mono**, so they're
  immediately recognizable as data rather than prose — this matters
  most in dense tables (e.g., the Officer's applicant list, the
  Company's shortlist).
- Where Inter is used for numbers inline in prose (e.g., "3 applicants
  shortlisted"), enable tabular figures (`font-variant-numeric:
  tabular-nums`) in table cells so columns of numbers align vertically.

### 4.5 Font Loading

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

Place this in `templates/shared/base.html`'s `<head>`, per the folder
structure in `03_Architecture.md` §4. For production, consider
self-hosting the font files in `static/` to avoid a runtime dependency
on Google Fonts' CDN (optional — Stretch-tier polish, not required for
MVP).

---

## 5. Component Theme Tokens

Supporting tokens to keep cards, buttons, and inputs consistent with
the palette above:

| Token | Value | Usage |
|---|---|---|
| `--radius-sm` | `6px` | Inputs, small buttons, badges |
| `--radius-md` | `10px` | Cards, modals |
| `--radius-lg` | `16px` | Hero/summary panels |
| `--shadow-sm` | `0 1px 2px rgba(17,24,39,0.06)` | Resting card elevation |
| `--shadow-md` | `0 4px 12px rgba(17,24,39,0.08)` | Hover/modal elevation |
| `--space-unit` | `4px` | Base spacing unit (use multiples: 8, 12, 16, 24, 32px) |

---

## 6. CSS Custom Properties Reference

Drop this into `static/css/theme.css` and import it before any other
stylesheet, per the structure in `03_Architecture.md` §4.

```css
:root {
  /* Primary & Accent */
  --color-primary: #2A9D8F;
  --color-accent: #2A9D8F;

  /* Neutrals & Layout */
  --color-background: #FDFBF7;
  --color-surface: #FDFBF7;
  --color-text-primary: #264653;
  --color-text-secondary: #8A6D3B;
  --color-border: #E9C46A;

  /* Status Colors */
  --status-applied: #2A9D8F;
  --status-shortlisted: #E9C46A;
  --status-interview: #E76F51;
  --status-selected: #2A9D8F;
  --status-rejected: #E76F51;

  /* Typography */
  --font-display: 'Sora', 'Segoe UI', system-ui, sans-serif;
  --font-body: 'Inter', 'Segoe UI', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Consolas', monospace;

  /* Radius & Shadow */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --shadow-sm: 0 1px 2px rgba(17, 24, 39, 0.06);
  --shadow-md: 0 4px 12px rgba(17, 24, 39, 0.08);

  /* Spacing */
  --space-unit: 4px;
}

body {
  background-color: var(--color-background);
  color: var(--color-text-primary);
  font-family: var(--font-body);
  font-size: 1rem;
  line-height: 1.6;
}

h1, h2, h3, h4 {
  font-family: var(--font-display);
  color: var(--color-text-primary);
}

.data-figure {
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
}
```

---

## 7. Implementation Notes

- These tokens live at the top of `static/css/`, imported once in
  `templates/shared/base.html`, so every app (`student_portal`,
  `company_portal`, `admin_portal`) inherits the same theme without
  redefining it.
- Status badge components should read their color from
  `--status-*` tokens keyed off the `Application.status` value (see
  §3.3's mapping table) — never hardcode a status color inline in a
  template.
- If Stretch-tier dark mode is ever considered (not in MVP scope per
  `02_Project_Requirements.md`), keep it to a second `:root[data-theme
  ="dark"]` block overriding these same token names, so components
  never need to know which theme is active.

---

## 8. Summary

Color is locked to the reference palette (deep teal, warm gold, terracotta, and soft cream with functional status colors mapped
one-to-one onto the SRS's application lifecycle). Typography adds a
deliberate identity — Sora for headings, Inter for body/UI, JetBrains
Mono for verified numeric data — while staying restrained enough for a
formal, trust-driven product. One accessibility fix is called out
explicitly (dark text on the amber "Under Review" badge); everything
else should be spot-checked against a contrast tool before final build.