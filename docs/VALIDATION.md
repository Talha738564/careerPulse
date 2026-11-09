# Validation and evidence

## Current checks
- 35 unittest cases pass across matching, required/preferred/zero-skill cases,
  route rendering, escaped input, combined filters, CSRF rejection, profile editing,
  browser isolation, shortlist idempotence, confirmed tracker updates/date checks,
  alert matching/deduplication, notification ownership/read state, password hashing,
  role guards, company references, opportunity lifecycle, URL verification and
  Oracle gateway bind/commit/rollback behavior using test doubles.
- `tests/browser_smoke.py` exercises real Chromium registration, login, profile and
  skill changes, matching, save, tracker updates, alerts, read notifications, logout,
  admin login, company creation, job creation and cross-account alert delivery.
- Nine student routes are checked for horizontal overflow at 390px. Desktop and
  mobile screenshots are captured; representative dashboard, tracker and admin
  screens are visually inspected. Keyboard skip-link focus and reduced-motion
  styling are checked. This is not a full screen-reader or real-device audit.
- Dependency consistency and Git whitespace checks pass.
- Oracle SQL parser checks and their limitations are documented separately in
  DATABASE_DESIGN.md. No Oracle integration test has executed.

## Issues caught and corrected
The real browser workflow exposed select controls whose label text included their
option text. Explicit accessible names now identify them reliably. Final review
also moved guest profile text out of signed cookies, fixed completed/rejected
application counts, replaced an unsupported arrow glyph, and ensured 16px mobile
form controls. Empty lists, missing records, rejected forms and expired CSRF tokens
have navigable states rather than silent failures.

## Remaining limitations
All web persistence is in-process demo memory, reset on restart. No Oracle server,
background notification worker, email delivery, password recovery, or production
hosting is configured. Password recovery and email delivery are not in this course
milestone's required scope. Live Oracle auth/persistence and concurrency tests are
pending a real database. Current tests do not establish production readiness.

Authentication discovery regression: homepage and header now expose Sign in and
Create account directly. Both forms were opened from the homepage at 1440px and
390px; /login/, /register/ and their canonical routes all return HTTP 200.

### Glass authentication refresh — 2026-11-01

Login and registration now use a dedicated responsive public layout with original brand artwork, bold headings, frosted forms and static blue/teal glass shapes. Existing authentication, CSRF, flash messages and server validation remain connected. Demo accounts still reset on server restart.

Validation: 35 unit tests passed; full Chromium student/admin browser workflow passed. Auth layout checked at 320, 390, 768 and 1440 CSS pixels with no horizontal overflow. Focused browser checks verified keyboard skip navigation, invalid login, password mismatch feedback and reduced-motion styling. Desktop and mobile screenshots were captured and visually inspected. Tests use browser emulation, not physical phones or their keyboards.

### Public homepage and navigation — 2026-11-08

Implemented the approved public landing concept with the original light-background
SVG logo, local Inter typography, working account/demo links and a reduced-motion
aware scroll reveal. Search now appears only on Explore, without a duplicate input.
Desktop workspace navigation can collapse, and the public page has a menu at all
sizes. Login emphasizes “here”; login/registration password fields have accessible
show/hide controls. Fonts and icons are served locally with licenses.

35 unit tests and the complete student/admin Chromium workflow pass. The focused
`tests/browser_landing.py` suite passes 80 route/width checks from 320px to 1440px,
checks menu keyboard behavior, password toggles, search placement, CTA navigation,
scroll reveal, reduced motion, no-JS fallback and browser errors. Visual comparison
and limitations are recorded in `design-qa.md`. Screenshots are generated in ignored
`artifacts/landing/`. These are browser-emulated checks, not physical-device tests.

Windows PowerShell:
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe tests/browser_smoke.py
.\.venv\Scripts\python.exe tests/browser_landing.py
```

Homepage follow-up: expanded the feature tour with job alerts, application tracking,
saved opportunities and deadline reminders, with working links to each existing tool.
Enlarged only the login “here” circle with three strokes. Re-ran all 35 unit tests and
80 route/viewport checks; feature links, all scroll reveals and no-JS/reduced-motion
behavior pass. Reviewed feature screenshots at 1440px and 390px.

Sidebar follow-up: run `python tests/browser_sidebar.py` for 72/240px widths, fixed
hamburger/nav coordinates, loaded SVGs, keyboard toggle/focus, active Settings,
mobile navigation and reduced motion. Passed at desktop widths 901–1920px and
mobile width 390px; screenshots are generated in `artifacts/sidebar/`. All 35 unit
tests and 80 existing responsive route checks also pass.

Dashboard/loading refresh: see [LOADING_PATTERNS.md](LOADING_PATTERNS.md) for the
architecture and Windows commands. `tests/browser_loading.py` exercises actual
held requests rather than simulated fixed delays: skeleton geometry, async search,
save and profile updates, history, request races, network failure recovery,
validation errors, responsive resizing, timing caps, inline icon loading,
reduced motion and no-JS fallback. `tests/browser_smoke.py` validates the complete
student/admin workflow, including skills, tracker and notifications.

Workspace/landing layout correction: `tests/browser_layout_fixes.py` verifies the
landing CTA buttons and “See how it works” fit without scrolling at 1366×768,
1440×900, 1280×720, 1024×600, 390×844, 360×640 and 320×568. It also verifies no
collapsed-rail vertical overflow at 500/640/900px heights, three workspace header
controls, guest/account menu access, Escape dismissal and authenticated sign-out.
The sidebar suite and full student/admin workflow also pass. Screenshots live in
`artifacts/layout-fixes/`. Mobile checks use browser emulation.

```powershell
.\.venv\Scripts\python.exe tests/browser_layout_fixes.py
```

Approved mobile header: logo, Sign in, Get started and menu share one row at
320–600px. The layout regression checks their shared vertical alignment and
retains 44px touch targets.
