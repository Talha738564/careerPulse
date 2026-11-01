# CareerPulse
A Flask + Jinja student opportunity-discovery and application-tracking project for
an individual Oracle DBMS course. HTML, custom CSS and native forms; no SPA, SQLite
fallback, scraper, employer accounts or in-app application submission.

## Run on Windows PowerShell
```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
if (!(Test-Path .env)) { Copy-Item .env.example .env }
.\.venv\Scripts\python.exe -m flask --app app:create_app run
```
Open http://127.0.0.1:5000. Use the homepage **Sign in** or **Create account** buttons for authentication,
or **Try the guest demo without an account** for a guest workspace.

For the admin workflow, set your own `ADMIN_EMAIL` and a unique `ADMIN_PASSWORD`
(12+ characters) in the ignored `.env`, restart, then sign in with them. The fixed
admin account is created at startup; public registration creates students only.
No default credentials are committed. Do not put credentials in screenshots.
Set a random `SECRET_KEY` in `.env` if you want a stable cookie-signing key. The
optional `COOKIE_SECURE=1` setting is for HTTPS only, not the local HTTP server.

## Working features
| Page | Behavior |
| --- | --- |
| `/` | Landing page and guest demo entry |
| `/register`, `/login` | Student registration, hashed passwords, sign-in |
| `/logout` | CSRF-protected POST logout |
| `/dashboard` | Ranked matches, skill demand, shortlist and tracker counts |
| `/profile` | Academic profile and skill proficiency/experience editing/reset |
| `/opportunities` | Search, type/city/skill/remote/pay/experience/deadline filters, sorting |
| `/opportunities/<id>` | Required/preferred skills, fit explanations, save/track controls |
| `/saved` | Isolated shortlist with idempotent save/remove |
| `/tracker` | Manual Saved/Applied/Interview/Offer/Rejected updates, dates and notes |
| `/alerts` | Create/edit/pause/delete skill-based alerts |
| `/notifications` | New matches, deadline reminders, read/unread views |
| `/admin/dashboard` | Protected catalog and student-interest analytics |
| `/admin/companies` | Create/edit/deactivate companies; delete unreferenced records |
| `/admin/opportunities` | Create/edit/expire/soft-remove roles and required/preferred skills |

Forms use POST and CSRF protection. Students cannot access admin routes. Apply
links open the employer website only for active, curator-verified real listings
whose HTTPS hostname matches the company careers site. The click is recorded as
analytics only; it never sets Applied. Fictional fixtures have no clickable apply
links. Manual tracker status changes require confirmation and application dates.

## Demo storage and limitations
All fixtures are fictional. Guest and signed-in profiles, accounts, catalog edits,
saved jobs, tracker entries, alerts and notifications are kept **in server memory**.
They reset when the process restarts. Guest identity and authentication use signed,
HTTP-only session cookies containing IDs/tokens, not profile text. Signing in starts
your account workspace; it does not import a guest shortlist. Use fictional data.
Run one process for the local course demo. This is not a public-production deployment.

An alert matches **any selected required skill** plus **all other criteria**; empty
skills means any skill. Existing catalog matches are included when an alert is saved.
Notifications deduplicate each alert/job event. Deadline reminders refresh when you
open notifications; there is no background worker or email delivery. Salary means
monthly pay for employment and project pay for freelance roles, so filter by job
type when comparing amounts.

Required-skill match = matched distinct required skills / total distinct required
skills × 100 (one decimal). Preferred skills do not count; zero requirements shows
**Not scored**. Git is never shown missing when present in the profile.

## Test
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe tests/browser_smoke.py
```
The browser test creates its own isolated app and fictional users; it never contacts
real employer sites. Screenshots go to ignored `artifacts/browser/` by default.
Use `--screenshots docs/screenshots` only to deliberately refresh committed evidence.

## Project structure
- `app.py`, `config.py`: app factory, shared profile/discovery routes and configuration.
- `routes/`: saved jobs, tracker, alerts, auth, protected admin, external apply.
- `services/`: fixture repository, profile validation, matching, activity, accounts,
  catalog validation and discovery. Presentation receives dictionaries for Jinja.
- `templates/`, `static/`: responsive UI and byte-identical original logo copies.
- `tests/`: service/route tests and an actual Chromium student/admin workflow.
- `db/`: Oracle schema, seeds, views, queries, transactions and a query gateway example.
- `docs/`: source brief, implementation history, DB design, validation and screenshots.

## Oracle status
`DATA_BACKEND=mock` is the supported mode. No Oracle database is currently available;
`DATA_BACKEND=oracle` fails explicitly rather than pretending persistence works.
The Oracle 19c+ schema, sample dataset, ERD, normalization discussion, SQL views,
queries and transaction examples are prepared. The optional gateway illustrates
bound queries and commit/rollback, but full application wiring and live verification
remain pending. See [database design](docs/DATABASE_DESIGN.md).

## Visual evidence
See [the screenshot gallery](docs/SCREENSHOTS.md) and [validation report](docs/VALIDATION.md).
All screenshots are rendered from this app; none are generated mockups.
