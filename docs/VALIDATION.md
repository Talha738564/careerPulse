# Validation and evidence

## Current checks
- 34 unittest cases pass across matching, required/preferred/zero-skill cases,
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
