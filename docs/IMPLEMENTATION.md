# Milestone 1

Routes: / (intro), /dashboard, /opportunities (GET q/type/remote filters),
/opportunities/<opp_id> (detail), and a shared 404 page.

app.create_app accepts a repository implementing the Protocol in
services/repository.py. Repository methods return fresh fictional dictionaries.
services/matching.py owns required-skill matching and demand aggregation;
templates receive presentation-ready values. Oracle implementation can join
COMPANIES, OPPORTUNITIES and OPPORTUNITY_SKILLS into this read interface. Student
skills come from STUDENT_SKILLS + SKILLS. Tracker rows map to APPLICATION_TRACKER.

Matched required skills / distinct required skills * 100, rounded to one decimal.
Preferred skills never count. Empty required sets return None (Not scored), not
100%. Sara knows Python, SQL, Git; Git is never shown missing for this profile.
Demand uses the fraction of catalog opportunities requiring each distinct skill.
Current fixtures are all active. A future Oracle adapter must filter active dates.

All records are fictional, read-only, and generated on each request. Dates are
relative to the server's current date. No employer links, credentials, auth,
persistence or application submission exist. Tracker counts are explicitly sample
activity; clicks never imply applications. Logo files are byte-identical copies.
No JavaScript is needed for this milestone; all navigation/filtering is native HTML.

Next: profile/skills editing with explicit demo storage semantics and CSRF-protected
POSTs; then saved jobs, manually confirmed tracker updates, alerts/notifications,
admin company/opportunity CRUD. Finally preserve the complete DBMS academic scope
in PROJECT_BRIEF.md with ERD, normalization, Oracle DDL/constraints, SQL demos,
authentication/authorization and a real Oracle adapter. Companies never log in.


## Milestone 2: demo profile and skills
`/profile` supports GET and validated POST; `/skills`, `/skills/remove`, and
`/profile/reset` accept CSRF-protected POST only. Profile fields cover name,
university, major, study year, CGPA (0–4 scale), city, resume/portfolio URLs and bio.
Skills support catalog selection, proficiency and years of experience; selecting
an existing skill updates it. Removing all skills is supported. Recommendations
and details use the edited skills immediately.

DemoProfileStore isolates temporary edits per signed browser cookie, not in Oracle.
Cookies are readable, not encrypted: use fictional data only. No login exists.
A random per-process signing key is used unless SECRET_KEY is configured locally;
restarts then invalidate sessions. Set your own random SECRET_KEY in .env for
restart persistence; never commit it. Reset restores the original fixtures.
Next milestone: saved jobs, then explicitly confirmed tracker status updates.

## Saved jobs
Save/remove actions are explicit, idempotent POSTs with CSRF protection. The saved
page and dashboard count reflect your shortlist. Per-visitor activity is held in
server memory for demo mode and resets on restart; no real application is implied.
Validation: 16 tests passed; saved page inspected at 1440px and 390px with no overflow.

## Application tracker
Students add entries as Saved and explicitly confirm every status update. Applied,
Interview, Offer and Rejected require an application date no later than today.
Notes, filters and removal are supported; adding again never overwrites progress.
18 tests passed; tracker desktop/mobile screenshots and overflow checks passed.

## Alerts and notifications
Create/edit/pause/delete alerts; match any selected required skill and all supplied
city/type/remote/minimum-pay criteria. Current catalog matches are included.
Notifications are deduplicated per alert/opportunity; saved deadlines within seven
days produce a separate reminder. Read state belongs to the visitor. 20 tests
passed, with captured desktop/mobile alert and notification pages.

## Authentication
Student registration, sign-in and POST logout use Werkzeug password hashes,
CSRF tokens, rotated login sessions and a five-attempt/minute sign-in limit.
Roles are assigned on the server; registration never creates administrators.
Configure ADMIN_EMAIL and ADMIN_PASSWORD (12+ characters) securely in local .env
before startup to create the fixed admin account. No default admin password exists.
Accounts and signed-in profiles are in memory in demo mode. Guest demo access is
intentional; guest sessions never inherit account activity. 23 tests passed.
