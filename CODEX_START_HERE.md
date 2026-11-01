# Initial instruction to paste into Codex

You are the lead implementation engineer for my **CareerPulse** project. I have **ALREADY created an empty GitHub repository and cloned it to my Windows computer**. I have now opened that cloned repository in Codex/VS Code. You must create the application folder structure and start building in this existing checkout. Do not run git init, create another repo, or change the existing origin remote.

**Before touching code:** inspect the current working folder, `git status`, current branch and `git remote -v`; read `AGENTS.md` and `docs/PROJECT_BRIEF.md` fully; inspect the four original SVG logo files under `brand/` and the optional screenshot. The handoff documents specify my business rules and desired look. If you are not in my cloned repository, tell me and stop rather than modifying another folder.

## Target and constraints
Build a premium, production-style but achievable **Flask + Jinja + HTML + CSS + vanilla JS** responsive website for a **2nd-year individual Oracle DBMS course project**. The app is a skill-based internship/job discovery and application tracker for students with admin-curated official opportunities. **Oracle is not configured for Codex yet**; start with believable clearly fictional mock data and a distinct adapter/repository layer so we can replace mocks with Oracle easily later. Do not use React, Next.js, Firebase, SQLite as a hidden replacement for Oracle, FastAPI, or a complex JS framework. Preserve the full DBMS scope (ERD, normalization, relational constraints, SQL demonstrations) for subsequent stages.

Use exactly the existing CareerPulse brand assets, with a navy/blue/teal visual identity. Implement **Modern SaaS + subtle glassmorphism**: mostly solid dark sidebar, clear white data cards, subtle translucent header/search, summary widgets and CTA surfaces. Design for both laptop/desktop and smartphone; mobile must have proper bottom navigation and reflowed content. Motion should be restrained, purposeful, accessible, and reduced-motion aware. Treat the screenshot as aesthetic reference, not a source of factual job data; use consistent fictional examples and current or clearly synthetic dates.

## Your first milestone: deliver working files, not just plans
1. Verify repository state; briefly summarize it and proposed files.
2. Create an organized Flask codebase (e.g. `app.py`, `config.py`, `templates/`, `static/css/`, `static/js/`, `static/images/`, `data/` or a small Python `services/` layer, `db/`, `tests/`, `docs/`, `requirements.txt`, `README.md`, `.env.example`, `.gitignore`). Adapt structure to Flask conventions, keep it approachable for a student.
3. Place/use original SVG logos in the app without modifying their artwork. Keep brand originals if desired.
4. Implement working Flask routes for `/`, `/dashboard`, `/opportunities` and `/opportunities/<opp_id>` using mock data aligned to project-brief fields.
5. Implement `base.html`, reusable responsive sidebar/topbar/mobile navigation, a professional student dashboard, and browse jobs/detail templates with believable fictional data, correct match calculations, matched/missing skill chips, skill demand presentation, tracker summary, empty states. Create navigation that works; avoid nonfunctional primary controls. For features not yet implemented, label them clearly or provide functional lightweight mock interactions rather than silent dead buttons.
6. Keep presentation independent from data access to support later Oracle queries. Set up `oracledb` dependency/config placeholders as appropriate but NEVER require working Oracle to run this first milestone.
7. Make a sensible light glass design with mobile responsive breakpoints. Include semantic HTML, keyboard/focus styles, sufficient color contrast, meaningful labels, reduced-motion support, no horizontal mobile overflow.
8. Provide run/setup instructions for Windows PowerShell. Test the app using Flask's test client or other available method, run any tests, check Jinja rendering and routes. If visual testing is available, capture and examine desktop and mobile screenshots; fix issues. Don't claim screenshots were checked if not.
9. Ensure `.gitignore` excludes `.env`, `.venv`, caches etc. Inspect git staging and then **make the first commit** `chore: scaffold CareerPulse Flask project`, followed by a feature commit if the dashboard is sufficiently complete. Since I want commits maintained, commit verified changes. Push to origin only if your environment is authenticated and you have my permission to push; otherwise give me the `git push -u origin main` command appropriate to the current branch. No force pushes.
10. Conclude with: exact files created, working routes, how to run, tests performed/results, commit hashes, mock limitations, and an actionable next milestone.

## After first milestone
Continue incrementally, not in one enormous rewrite: profile and student skills; saved jobs; tracker with manually confirmed application status; job alerts and notifications; admin dashboard and CRUD screens; then Oracle SQL schema, matching queries, proper auth and real integration. Make one coherent Git commit per meaningful tested feature. Respect the project brief's company/admin boundaries and no auto-submitted applications.

## Additional critical details
- Required skill match score = count of matched required skills / total required skills × 100; preferred skills not in denominator. Explain handling of zero required skills.
- The example in the source brief that says a student has Git AND is missing Git is inconsistent; correct the illustrative demo data without altering the algorithm.
- An external apply URL click does NOT mean a real application was submitted. Ask for explicit student status update.
- Don't invent my Oracle service name/password; retain `.env.example` placeholders.
- No actual links to employer job postings unless verified. Fictional opportunities should have non-clickable sample apply links or be labeled demo; do not present fictional links as real.
- I am building this individually. Favor simple, understandable code and a professional look over unnecessary complexity.

Start executing the first milestone now. Do not ask me to create the folder structure manually; you are responsible for doing that in this cloned repository.
