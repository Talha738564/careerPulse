# CareerPulse
Flask + Jinja student career discovery demo for an individual Oracle DBMS project.

## Windows PowerShell
```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m flask --app app:create_app run
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
Open http://127.0.0.1:5000. No Oracle connection is required. Only copy .env if it
does not already exist. The development server is for local use, not production.

## First milestone
- `/`: introduction and demo entry
- `/dashboard`: ranked recommendations, skill demand and sample tracker
- `/opportunities`: search by role/company/city/skill, job type and remote filters
- `/opportunities/<opp_id>`: required/preferred skills and match explanation

All data is fictional. Profile edits are temporary browser-session data. No real
applications or Oracle writes occur. Saved jobs, tracker editing, alerts and admin
workflows are future work.
Zero required skills means **Not scored**. See docs/IMPLEMENTATION.md for the
adapter contract, limitations and next milestones. Original brand artwork is
copied unchanged. No external fonts, scripts or frontend build are required.


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
