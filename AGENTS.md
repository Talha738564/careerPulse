# CareerPulse — Codex project instructions

## Mission and current state
CareerPulse is an individual second-year DBMS course project: a skill-based internship, freelance and entry-level job discovery platform. Oracle database design/SQL/normalization are the primary academic goals; a functional Flask + Jinja web application is the demonstration layer. The user already created an EMPTY GitHub repository and CLONED IT LOCALLY. Work in the existing cloned repository. NEVER run `git init`, replace the remote, create a second repository, or overwrite the user's repo metadata. Start by inspecting `pwd`, files, `git status`, `git remote -v`, and current branch. If the clone is not the working directory, stop and tell the user how to open it. Do not hallucinate existing code.

## Source of truth
Read `docs/PROJECT_BRIEF.md` (supplied in the handoff bundle) thoroughly before implementing functionality or database changes. This document defines the scope, entities, SQL and user workflows. Where this instruction and project brief differ, preserve the brief's feature scope and database-first academic requirements, while following the explicitly agreed **frontend-first implementation sequencing** described below. Flag contradictions and propose the smallest viable correction rather than silently changing product requirements.

## Scope and users
Students register/login, edit academic profile (university, major, study year, CGPA, city, resume/portfolio URLs, bio), manage skills/proficiency/experience, browse/search/filter admin-curated opportunities, view a *required-skill* match score and lists of matched/missing skills, save jobs, open official employer apply URL, manually track application status, create alerts, and read notifications. Administrator has a fixed administrative account and curates companies/opportunities, job skills, verified links and simple analytics. Companies are **database entities only**; they do not register or post jobs. Do NOT add employer logins, in-app application submission, hiring decisions, messaging, automated website scraping, resume builders, AI cover-letter generation, Firebase, React, FastAPI, or other unrelated frameworks.

## Stack and architecture
- Python 3.x + Flask; server-rendered Jinja templates; HTML, custom CSS, minimal vanilla JS; optional Bootstrap only if it clearly improves consistency; no heavy SPA dependency.
- Oracle Database via `python-oracledb` for later real data. Oracle SQL Developer is only a GUI database client, not the database. No university DB connection is assumed. Host/port/service/username are unknown until user supplies real settings.
- Localhost-first application, Windows and VS Code friendly.
- Use `.env` for secrets, commit only `.env.example` with placeholders. Do not commit credentials, local databases, sessions, `.venv`, caches, or actual personal student data.
- Keep database access in a dedicated module and view routes separate from data logic. Use service/repository boundaries or equivalent, so demo/mock fixtures are replaceable by Oracle queries without rewriting templates.
- Use routes/forms/templates that map to the project brief. Do not introduce routes that change the underlying business rules.

## Database contract (not necessarily implemented on Day 1)
The intended tables: USERS, STUDENTS, SKILLS, STUDENT_SKILLS, COMPANIES, OPPORTUNITIES, OPPORTUNITY_SKILLS, SAVED_JOBS, APPLICATION_TRACKER, JOB_ALERTS, JOB_ALERT_SKILLS, NOTIFICATIONS, and optional APPLY_CLICKS, SKILL_RESOURCES. Full fields, constraints, associations and DDL are in `docs/PROJECT_BRIEF.md`. Mock records should use the same conceptual field names as DB columns, including `opp_id`, `company_id`, `job_type`, `is_remote`, `status`, `apply_url`, `posted_at`, `deadline`. Job match score is required skills known / total required skills × 100; preferred skills are not counted. Define behavior for zero required skills explicitly, not by division by zero. Never invent production Oracle credentials or claim real data is connected when it is mocked. Don't silently treat external apply-link clicks as completed applications: mark `APPLIED` only after user confirmation. Reconcile the brief's contradictory example where a student both knows Git and is missing Git.

## Design source / identity
The official SVG assets are provided in `brand/`:
- `careerpulse_primary_logo_lockup.svg`
- `careerpulse-icon-static.svg`
- `careerpulse_logo_variants_and_small_sizes.svg`
- `careerpulse_icon_draw_animation_preview.svg`
Use these ORIGINAL files; do not recreate, recolor, distort, or substitute the logo without explicit user approval. An optional image reference is `brand/reference-dashboard.png`; use as conceptual inspiration, not as existing HTML or an exact implementation requirement. Original brand uses a pulse-to-upward-arrow symbol, deep navy, blue, teal. Extract precise colors from source SVGs where useful rather than guessing.

## UI direction: Modern career SaaS + restrained soft glassmorphism
Target clean, premium, responsive, accessible student job-discovery UI. Deep navy mostly solid sidebar; blue actions; teal match/progress; near-white background; white job and chart cards; organized neutral borders and soft shadows. Use soft glass selectively for sticky top header/search, 4 overview stats, profile/CTA/banner, overlays and mobile filter bottom sheet. Avoid blanket glass on dense job listings/charts/tracker. Maintain readable contrast and fallback for unsupported backdrop-filter. Avoid neon, oversized 3D, moving backgrounds, heavy blur, decorative visual noise. Use a reusable token-based CSS system (spacing, typography, colors, shadows, radii). Prefer Inter or other sensible system font fallback; no unapproved remote fonts required for local demo.

## Desktop / mobile behavior
Desktop: left sidebar, top search/header, responsive stats row, recommended jobs, skill matches + matched/missing explanations, demand charts, application tracker summary. Job discovery may use split list-detail view where practical. Mobile: replace sidebar with compact header and 4–5-item bottom navigation (Home, Explore, Saved, Tracker, Profile), stack cards vertically, horizontal scroller for overview metrics only if accessible, filter bottom sheet/drawer, no horizontal page overflow, comfortable touch targets. Include tablet breakpoint. Never shrink the full desktop dashboard into an unreadable mobile replica.

## Motion guidelines
Use purposeful, small CSS transitions: hover/press feedback ~100–160 ms, dropdowns ~150–250 ms, drawers ~200–300 ms. Animate mostly transform and opacity, not layout sizes. Consider a one-shot logo draw animation only for appropriate first-load context, not continuous on every page. Honor `prefers-reduced-motion`; provide non-hover affordances on touch. No constant chart animation or animated text during reading. CSS first; do not add heavy animation libraries.

## Required page inventory
Public: landing, login, student registration. Student: dashboard, profile/skills, explore opportunities, opportunity details/matched-missing skills, saved, application tracker (Saved, Applied, Interview, Offer, Rejected), alerts, notifications. Admin: dashboard, companies CRUD screens, opportunities CRUD and skills form. Build a coherent layout system and incrementally implement pages; do NOT dump all pages in one giant change.

## Development sequence for the limited frontend opportunity
1. Inspect repo and provided files, reproduce agreed scope. Establish Flask scaffold and simple mock-data mode.
2. Implement design tokens, responsive Jinja base template, original logo placement, desktop sidebar, mobile nav, accessible components.
3. Implement real navigable student dashboard with realistic *fictional* aligned data and meaningful interactive UI states.
4. Implement explore/search/filters, job detail and skill gap, bookmarks, application tracker, profile/skills, alerts/notifications.
5. Implement admin views/forms. Avoid fake claims that forms persist to Oracle; mock writes only if explicitly labeled.
6. Test and document mobile/desktop, keyboard access, empty/loading/error states. Define API/data contracts and Oracle integration map.
7. Then implement Oracle schema/seed scripts, normalization, SQL views, queries, Flask database services, authentication and integration, following project brief. This project is DBMS-FIRST academically even when UI is built first temporally.

## Code quality, security, and testing
Separate templates, static assets, Python modules, config, mock fixtures, SQL scripts, docs. Escape user input via Jinja defaults, use parameterized SQL (never f-string SQL), hashed passwords, safe sessions, auth/role guards, POST+CSRF protection for mutations, validate official apply links and redirect safely, avoid untrusted external redirects. Do not use Flask debug=True in production. Include reusable error states and basic automated tests for core logic where possible. If Oracle isn't available, provide mock mode and report integration as pending, not "working".

## Git operating rules
The repo was already cloned from GitHub. Preserve `origin` and branch. Inspect state before editing. Create `.gitignore` early. First substantive commit: `chore: scaffold CareerPulse Flask project`. Subsequent small, meaningful commits, e.g. `style: establish responsive CareerPulse design system`, `feat: implement student dashboard with mock data`, `feat: add opportunity search and detail views`. Before each commit inspect `git status`, `git diff`, and `git diff --cached`; run relevant tests/lint/smoke check. Do not include credentials or irrelevant files. Commit when asked/authorized; push to `origin` only if authenticated and user authorized pushing; never force-push or rewrite history. Do not claim commit/push succeeded unless the shell confirmed it. Summarize each commit hash and unfinished tasks.

## Collaboration style
Implement actual working files, don't merely describe code. Work in small reviewable milestones. Before major changes, state file plan; after implementation give actual commands for Windows PowerShell to run and test. Don't ask user to recreate folder structure manually. If credentials/Oracle instance are absent, build mock-data mode and defer Oracle integration. No invented live job postings or dates; clearly label fictional seed data. If key facts are missing, use safe placeholders and document them.
