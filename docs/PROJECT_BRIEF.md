Below is your **complete, finalized project brief**. Copy everything from the next line into any LLM as a prompt/context document.

***

# PROJECT BRIEF: CareerPulse

## 1. Project identity

**Project name:** CareerPulse  
**Full title:** CareerPulse – Skill-Based Internship & Job Discovery Platform  
**Project type:** Individual Database Management Systems course project  
**Student level:** 2nd Year, Computer Science  
**Primary focus:** Database design, SQL, normalization, and Oracle implementation  
**Secondary focus:** A functional Flask web application for demonstration  
**Deployment target:** Localhost for course demo; optional online hosting later  

## 2. One-paragraph summary

CareerPulse is a web-based platform that helps university students discover relevant internships, freelance gigs, and entry-level jobs through skill-based matching, personalized job alerts, and a personal application tracker. An administrator curates real opportunities from official company career pages and LinkedIn, storing the job details, required skills, source, and the company’s official external application URL. Students create skill profiles, browse and filter opportunities, view a skill-match score and missing-skill gaps, receive notifications for relevant new jobs, open the official application page through an “Apply on Company Website” button, and track their own application progress. CareerPulse does **not** host applications, make hiring decisions, or auto-submit forms on external websites; it is a discovery, matching, alerting, and tracking layer that directs students to official employer application pages.

## 3. Problem statement

Students often find internship and job opportunities scattered across LinkedIn, company career pages, and multiple job boards. They waste time searching manually, applying to poorly matched roles, and losing track of where they applied. Existing platforms are either too broad, too competitive, or not tailored to early-career students.

CareerPulse solves this by:

- Centralizing curated internship and job opportunities.
- Matching opportunities to each student’s skills.
- Showing missing skills, not just a match percentage.
- Sending alerts when relevant opportunities are posted.
- Providing a personal application tracker.
- Directing students only to official application links.

This follows the standard job-aggregator model: aggregate and organize listings, help users filter and discover relevant roles, then direct them to the employer’s own application URL. [testlify](https://testlify.com/job-aggregator/)

## 4. Users and roles

### Student

A student can:

- Register and log in.
- Create and edit a profile: university, major, study year, CGPA, city, resume URL, portfolio URL, and bio.
- Add skills with proficiency level and years of experience.
- Browse and search opportunities.
- Filter by skill, job type, city, remote status, salary, experience level, and deadline.
- View a job detail page with description, requirements, company information, source, and official apply link.
- See a **Skill Match Score** and **Skill Gap Radar** for each job.
- Save a job.
- Click **Apply on Company Website**, which opens the official external application URL in a new tab.
- Track the job personally: Saved → Applied → Interview → Offer / Rejected.
- Create job alerts based on skills, city, remote preference, job type, and salary.
- Receive in-app notifications when a new matching job is posted or a saved job deadline is near.

### Administrator

The admin is the platform curator, not an employer. The admin can:

- Log in with a fixed admin account.
- Add, edit, deactivate, or remove companies.
- Add, edit, expire, or remove opportunities.
- Attach required/preferred skills to opportunities.
- Add the official external application URL and source for each job.
- Mark opportunities as verified where the link comes from an official company careers page.
- View platform statistics: total jobs, active jobs, most demanded skills, most saved jobs, and most-clicked apply links.

The admin does **not**:

- Accept or reject candidates.
- Conduct interviews.
- Make hiring decisions.
- Host application forms.
- Auto-fill or submit applications on company websites.

### Companies

Companies are **database entities only**. They do not register, log in, post jobs, or review candidates inside CareerPulse. Their information and official career/apply links are curated by the admin.

This avoids the unrealistic workflow where an admin would accept or shortlist a student on a company’s behalf.

## 5. Core features

### Must-have features

1. **Student authentication**
   - Register, login, logout.
   - Password stored securely as a hash.
   - Role-based access: student and admin.

2. **Student skill profile**
   - Add/remove skills.
   - Set proficiency: Beginner, Intermediate, Advanced.
   - Set years of experience.
   - Update academic and profile information.

3. **Curated opportunity catalog**
   - Admin adds opportunities with company, title, type, description, requirements, city, remote flag, salary range, experience level, deadline, source, and official apply URL.
   - Opportunities have required and preferred skills.

4. **Search and filtering**
   - Search by title, company, skill, or description.
   - Filter by job type, city, remote, salary, experience level, and active deadline.

5. **Skill Match Score**
   - For each opportunity, calculate:

\[
\text{Match Score} =
\frac{\text{Required skills known by student}}{\text{Total required skills}} \times 100
\]

   - Example: a job requires Python, SQL, and Git; the student knows Python and SQL, so the score is 66.7%.
   - Skills-based matching is a recognized approach for identifying candidate-job alignment. [linkedin](https://www.linkedin.com/help/recruiter/answer/a592622)

6. **Skill Gap Radar**
   - Shows required skills the student does not have.
   - Example: “You match Python and SQL. Missing: Git, Docker.”
   - This turns the platform into a career-development tool, not only a job list. [jobagent](https://www.jobagent.sh/docs)

7. **Smart job alerts**
   - Student creates an alert such as: “Python + SQL + Lahore + Internship.”
   - When the admin adds a matching opportunity, the system creates an in-app notification.
   - Job alerts normally monitor new listings against user-defined criteria such as role, location, job type, and keywords. [isolvedhcm](https://www.isolvedhcm.com/glossary/job-alerts)

8. **External apply workflow**
   - Each job has an official `apply_url`.
   - The student clicks **Apply on Company Website**.
   - The link opens in a new tab.
   - CareerPulse records the click and optionally creates/updates a tracker entry.
   - The student completes the real application on the company’s site.
   - This mirrors the common external-apply model used by job platforms. [indeed](https://www.indeed.com/hire/resources/howtohub/optimize-jobs-from-your-career-site-or-ats-on-indeed)

9. **Personal application tracker**
   - Student manually updates status:
     - Saved
     - Applied
     - Interview
     - Offer
     - Rejected
   - Student can add notes and dates.
   - This is useful because the actual application occurs outside CareerPulse. [linkedin](https://www.linkedin.com/help/recruiter/answer/a414058)

### Differentiating features

Choose **at least two** of these for a stronger project:

1. **Deadline Pulse**
   - Highlights jobs closing within 7 days.
   - Sends a deadline reminder notification.

2. **Trending Skills dashboard**
   - Shows the most demanded skills across active jobs.
   - Example: “SQL appears in 45% of active internships.”

3. **Company Trust Badge**
   - Marks opportunities whose apply link comes from an official company careers page.
   - Helps reduce fake or unofficial listings.

4. **Job Fit Explanation**
   - Instead of only “67% match,” show:
     - Matched: Python, SQL
     - Missing: Git
   - More useful than a bare percentage. 

5. **Learn Missing Skill suggestions**
   - For each missing skill, show a curated course/documentation link.
   - Example: Missing Docker → link to Docker documentation or a beginner course.

## 6. Explicit project boundaries

To keep the project realistic and feasible for one student:

- CareerPulse will **not** host job applications.
- CareerPulse will **not** make hiring decisions.
- CareerPulse will **not** allow companies to log in or post jobs.
- CareerPulse will **not** auto-fill or auto-submit external application forms.
- CareerPulse will **not** scrape websites automatically; the admin will manually curate opportunities.
- CareerPulse will **not** include messaging, resume builders, or AI cover-letter generation in the first version.

These boundaries should be written clearly in the project report as deliberate scope decisions.

## 7. Technology stack

| Layer | Technology |
|---|---|
| Database | Oracle Database |
| Backend | Python with Flask |
| Frontend | HTML, CSS, JavaScript |
| Styling | Bootstrap or custom CSS |
| Database access | Python Oracle driver, e.g., `oracledb` |
| Authentication | Flask session-based login with hashed passwords |
| Version control | Git and GitHub |
| Documentation | Microsoft Word / Google Docs |
| Demo data | SQL seed scripts with realistic fictional/sample data |

## 8. Database design

### Entities

1. **USERS**  
   Stores all system accounts: students and admin.

2. **STUDENTS**  
   Stores student-specific academic and profile information.

3. **SKILLS**  
   Master list of skills, such as Python, SQL, Java, Git, Docker, Graphic Design.

4. **STUDENT_SKILLS**  
   Many-to-many relationship between students and skills, including proficiency and experience.

5. **COMPANIES**  
   Stores company profiles, official website, careers page, city, verification status, and description.

6. **OPPORTUNITIES**  
   Stores curated internships, gigs, and jobs. Includes the official external apply URL and source.

7. **OPPORTUNITY_SKILLS**  
   Many-to-many relationship between opportunities and skills, with required/preferred importance.

8. **SAVED_JOBS**  
   Stores jobs saved by students.

9. **APPLICATION_TRACKER**  
   Stores each student’s personal application status and notes for a job.

10. **JOB_ALERTS**  
   Stores student-defined alert criteria.

11. **JOB_ALERT_SKILLS**  
   Links alerts to the skills the student wants to be notified about.

12. **NOTIFICATIONS**  
   Stores in-app notifications for new matching jobs, deadline reminders, and system messages.

13. **APPLY_CLICKS**  
   Optional analytics table recording when a student clicks the external apply link.

14. **SKILL_RESOURCES**  
   Optional table linking missing skills to learning resources.

### Relationships

- One `USER` may have one `STUDENT` profile.
- One `STUDENT` may have many `STUDENT_SKILLS`.
- One `SKILL` may belong to many `STUDENT_SKILLS`.
- One `COMPANY` may have many `OPPORTUNITIES`.
- One `OPPORTUNITY` may have many `OPPORTUNITY_SKILLS`.
- One `SKILL` may be required by many `OPPORTUNITY_SKILLS`.
- One `STUDENT` may save many `OPPORTUNITIES`.
- One `OPPORTUNITY` may be saved by many `STUDENTS`.
- One `STUDENT` may have many `APPLICATION_TRACKER` records.
- One `OPPORTUNITY` may appear in many `APPLICATION_TRACKER` records.
- One `STUDENT` may create many `JOB_ALERTS`.
- One `JOB_ALERT` may include many skills through `JOB_ALERT_SKILLS`.
- One `USER` may receive many `NOTIFICATIONS`.
- One `OPPORTUNITY` may generate many notifications.

## 9. Oracle table structure

Use these tables as the starting schema. Adjust data types and sizes as needed for your Oracle version.

```sql
-- USERS
CREATE TABLE users (
  user_id        NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  full_name      VARCHAR2(120) NOT NULL,
  email          VARCHAR2(150) NOT NULL UNIQUE,
  password_hash  VARCHAR2(255) NOT NULL,
  role           VARCHAR2(20) NOT NULL CHECK (role IN ('STUDENT','ADMIN')),
  created_at     DATE DEFAULT SYSDATE NOT NULL,
  is_active      CHAR(1) DEFAULT 'Y' CHECK (is_active IN ('Y','N'))
);

-- STUDENTS
CREATE TABLE students (
  student_id     NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  user_id        NUMBER NOT NULL UNIQUE REFERENCES users(user_id),
  university     VARCHAR2(150),
  major          VARCHAR2(120),
  study_year     NUMBER,
  cgpa           NUMBER(4,2),
  city           VARCHAR2(100),
  resume_url     VARCHAR2(500),
  portfolio_url  VARCHAR2(500),
  bio            VARCHAR2(1000)
);

-- SKILLS
CREATE TABLE skills (
  skill_id       NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  skill_name     VARCHAR2(100) NOT NULL UNIQUE,
  category       VARCHAR2(80)
);

-- STUDENT_SKILLS
CREATE TABLE student_skills (
  student_skill_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  student_id       NUMBER NOT NULL REFERENCES students(student_id),
  skill_id         NUMBER NOT NULL REFERENCES skills(skill_id),
  proficiency      VARCHAR2(20) DEFAULT 'BEGINNER'
                   CHECK (proficiency IN ('BEGINNER','INTERMEDIATE','ADVANCED')),
  years_experience NUMBER(3,1) DEFAULT 0,
  CONSTRAINT uq_student_skill UNIQUE (student_id, skill_id)
);

-- COMPANIES
CREATE TABLE companies (
  company_id       NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  company_name     VARCHAR2(150) NOT NULL,
  industry         VARCHAR2(100),
  website_url      VARCHAR2(500),
  careers_page_url VARCHAR2(500),
  city             VARCHAR2(100),
  is_verified      CHAR(1) DEFAULT 'N' CHECK (is_verified IN ('Y','N')),
  description      VARCHAR2(2000)
);

-- OPPORTUNITIES
CREATE TABLE opportunities (
  opp_id            NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  company_id        NUMBER NOT NULL REFERENCES companies(company_id),
  title             VARCHAR2(200) NOT NULL,
  job_type          VARCHAR2(20) NOT NULL
                    CHECK (job_type IN ('INTERNSHIP','FREELANCE','FULL_TIME')),
  description       VARCHAR2(4000),
  requirements      VARCHAR2(4000),
  city              VARCHAR2(100),
  is_remote         CHAR(1) DEFAULT 'N' CHECK (is_remote IN ('Y','N')),
  min_salary        NUMBER(12,2),
  max_salary        NUMBER(12,2),
  experience_level  VARCHAR2(30)
                    CHECK (experience_level IN ('STUDENT','FRESH','JUNIOR')),
  apply_url         VARCHAR2(500) NOT NULL,
  source_name       VARCHAR2(150),
  posted_at         DATE DEFAULT SYSDATE NOT NULL,
  deadline          DATE,
  status            VARCHAR2(20) DEFAULT 'ACTIVE'
                    CHECK (status IN ('ACTIVE','EXPIRED','REMOVED'))
);

-- OPPORTUNITY_SKILLS
CREATE TABLE opportunity_skills (
  opp_skill_id  NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  opp_id        NUMBER NOT NULL REFERENCES opportunities(opp_id),
  skill_id      NUMBER NOT NULL REFERENCES skills(skill_id),
  importance    VARCHAR2(20) DEFAULT 'REQUIRED'
                CHECK (importance IN ('REQUIRED','PREFERRED')),
  CONSTRAINT uq_opp_skill UNIQUE (opp_id, skill_id)
);

-- SAVED_JOBS
CREATE TABLE saved_jobs (
  saved_id    NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  student_id  NUMBER NOT NULL REFERENCES students(student_id),
  opp_id      NUMBER NOT NULL REFERENCES opportunities(opp_id),
  saved_at    DATE DEFAULT SYSDATE NOT NULL,
  CONSTRAINT uq_saved_job UNIQUE (student_id, opp_id)
);

-- APPLICATION_TRACKER
CREATE TABLE application_tracker (
  tracking_id   NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  student_id    NUMBER NOT NULL REFERENCES students(student_id),
  opp_id        NUMBER NOT NULL REFERENCES opportunities(opp_id),
  status        VARCHAR2(20) NOT NULL DEFAULT 'SAVED'
                CHECK (status IN ('SAVED','APPLIED','INTERVIEW','OFFER','REJECTED')),
  applied_on    DATE,
  notes         VARCHAR2(1000),
  last_updated  DATE DEFAULT SYSDATE NOT NULL,
  CONSTRAINT uq_tracker_student_opp UNIQUE (student_id, opp_id)
);

-- JOB_ALERTS
CREATE TABLE job_alerts (
  alert_id       NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  student_id     NUMBER NOT NULL REFERENCES students(student_id),
  alert_name     VARCHAR2(150) NOT NULL,
  city           VARCHAR2(100),
  is_remote_only CHAR(1) DEFAULT 'N' CHECK (is_remote_only IN ('Y','N')),
  job_type       VARCHAR2(20)
                 CHECK (job_type IN ('INTERNSHIP','FREELANCE','FULL_TIME')),
  min_salary     NUMBER(12,2),
  created_at     DATE DEFAULT SYSDATE NOT NULL,
  is_active      CHAR(1) DEFAULT 'Y' CHECK (is_active IN ('Y','N'))
);

-- JOB_ALERT_SKILLS
CREATE TABLE job_alert_skills (
  alert_skill_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  alert_id       NUMBER NOT NULL REFERENCES job_alerts(alert_id),
  skill_id       NUMBER NOT NULL REFERENCES skills(skill_id),
  CONSTRAINT uq_alert_skill UNIQUE (alert_id, skill_id)
);

-- NOTIFICATIONS
CREATE TABLE notifications (
  notification_id  NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  user_id          NUMBER NOT NULL REFERENCES users(user_id),
  opp_id           NUMBER REFERENCES opportunities(opp_id),
  title            VARCHAR2(200) NOT NULL,
  message          VARCHAR2(1000) NOT NULL,
  notification_type VARCHAR2(30) NOT NULL
                   CHECK (notification_type IN ('NEW_MATCH','DEADLINE_SOON','SYSTEM')),
  is_read          CHAR(1) DEFAULT 'N' CHECK (is_read IN ('Y','N')),
  created_at       DATE DEFAULT SYSDATE NOT NULL
);

-- APPLY_CLICKS
CREATE TABLE apply_clicks (
  click_id   NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  student_id NUMBER NOT NULL REFERENCES students(student_id),
  opp_id     NUMBER NOT NULL REFERENCES opportunities(opp_id),
  clicked_at DATE DEFAULT SYSDATE NOT NULL
);

-- SKILL_RESOURCES
CREATE TABLE skill_resources (
  resource_id    NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  skill_id       NUMBER NOT NULL REFERENCES skills(skill_id),
  resource_title VARCHAR2(200) NOT NULL,
  resource_url   VARCHAR2(500) NOT NULL,
  resource_type  VARCHAR2(30)
                 CHECK (resource_type IN ('COURSE','YOUTUBE','DOCUMENTATION','ARTICLE')),
  difficulty     VARCHAR2(20)
                 CHECK (difficulty IN ('BEGINNER','INTERMEDIATE','ADVANCED'))
);
```

## 10. Important SQL features to demonstrate

Your report and demo should include:

- **ER diagram** and explanation of cardinalities.
- **Normalization:** show progression from unnormalized data to 1NF, 2NF, 3NF, and preferably BCNF.
- **Primary keys, foreign keys, unique constraints, check constraints, and not-null constraints.**
- **Joins:** student skills joined with opportunity skills for match calculation.
- **Aggregations:** skill demand, jobs per company, average salary by job type.
- **Subqueries:** jobs requiring skills the student lacks; jobs with above-average salary.
- **Views:**
  - `v_active_opportunities`
  - `v_student_skill_profile`
  - `v_opportunity_skill_summary`
  - `v_student_job_matches`
- **Indexes:**
  - `opportunities(status, deadline)`
  - `opportunities(city)`
  - `opportunity_skills(skill_id)`
  - `student_skills(student_id)`
  - `notifications(user_id, is_read)`
- **Transactions:** inserting an opportunity with its skills, or creating a tracker record and notification together.
- **Optional advanced objects, if taught:** triggers, procedures, functions, sequences, and cursors.

## 11. Main user workflows

### Workflow 1: Student finds and applies to a job

1. Student registers and logs in.
2. Student adds skills: Python, SQL, Git.
3. Student browses jobs and filters by “Python” and “Internship.”
4. Student opens a Python Backend Intern job.
5. CareerPulse shows:
   - Match Score: 67%
   - Matched skills: Python, SQL
   - Missing skills: Git
6. Student clicks **Apply on Company Website**.
7. CareerPulse opens the official company application URL in a new tab.
8. CareerPulse records the click and creates a tracker entry with status `APPLIED`.
9. Student later updates the tracker to `INTERVIEW` or `REJECTED`.

### Workflow 2: Student receives a smart alert

1. Student creates an alert:
   - Skills: Python, SQL
   - City: Lahore
   - Job type: Internship
   - Remote: Any
2. Admin adds a new internship from Arbisoft requiring Python, SQL, and Git.
3. CareerPulse compares the job’s required skills with the student’s skills.
4. Since the student matches Python and SQL, the system creates a notification:
   - “New Python Backend Internship at Arbisoft matches 2 of your skills.”
5. Student opens the notification and views the job.

### Workflow 3: Admin curates a job

1. Admin logs in.
2. Admin adds or selects a company, e.g., Arbisoft.
3. Admin adds a job:
   - Title: Python Backend Intern
   - Type: Internship
   - City: Lahore or Remote
   - Required skills: Python, SQL, Git
   - Source: Arbisoft Careers Page
   - Apply URL: official Arbisoft application page
   - Deadline: a future date
4. CareerPulse checks active student alerts.
5. Matching students receive notifications.

## 12. Sample seed data plan

Create realistic sample data such as:

- 1 admin account.
- 15–25 student accounts.
- 8–12 companies, including realistic but clearly educational entries inspired by companies such as NetSol, Devsinc, Arbisoft, and Systems.
- 25–40 opportunities.
- 10–20 skills.
- 40–80 student-skill records.
- 20–40 saved jobs.
- 20–40 tracker records.
- 5–10 job alerts.
- 20–50 notifications.

Clearly state in the report that company and opportunity data are inspired by publicly available information and used only for academic purposes; no official affiliation is implied.

## 13. Flask application structure

Use a simple structure like this:

```text
careerpulse/
│
├── app.py
├── config.py
├── requirements.txt
│
├── db/
│   ├── schema.sql
│   ├── seed_data.sql
│   └── queries.sql
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       └── careerpulse_logo.png
│
└── templates/
    ├── base.html
    ├── home.html
    ├── login.html
    ├── register.html
    ├── student_dashboard.html
    ├── profile.html
    ├── opportunities.html
    ├── opportunity_detail.html
    ├── alerts.html
    ├── tracker.html
    ├── notifications.html
    └── admin/
        ├── admin_dashboard.html
        ├── manage_companies.html
        ├── manage_opportunities.html
        └── opportunity_form.html
```

## 14. Main Flask routes

| Route | Purpose |
|---|---|
| `/` | Home / landing page |
| `/register` | Student registration |
| `/login` | Login |
| `/logout` | Logout |
| `/dashboard` | Student dashboard |
| `/profile` | View/edit student profile |
| `/skills` | Manage student skills |
| `/opportunities` | Browse/search/filter jobs |
| `/opportunities/<opp_id>` | Job detail page |
| `/opportunities/<opp_id>/save` | Save or unsave job |
| `/opportunities/<opp_id>/apply-external` | Record apply click and redirect to official URL |
| `/tracker` | View/update personal application tracker |
| `/alerts` | Create/manage job alerts |
| `/notifications` | View notifications |
| `/admin/dashboard` | Admin dashboard |
| `/admin/companies` | Manage companies |
| `/admin/opportunities` | Manage opportunities |
| `/admin/opportunities/new` | Add new opportunity |
| `/admin/opportunities/<opp_id>/edit` | Edit opportunity |

## 15. Build order

Follow this sequence:

1. **Finalize requirements**
   - Confirm features, roles, and boundaries.

2. **Design the database**
   - Draw the ER diagram.
   - Normalize the design.
   - Create the Oracle schema.

3. **Create seed data**
   - Insert admin, skills, students, companies, opportunities, alerts, and notifications.

4. **Write core SQL**
   - Job search queries.
   - Match-score query.
   - Skill-gap query.
   - Trending-skills query.
   - Deadline query.
   - Notification-generation query.

5. **Build Flask backend**
   - Database connection.
   - Authentication.
   - Student profile and skills.
   - Opportunity browsing.
   - Job detail page.
   - External apply redirect and tracker.
   - Alerts and notifications.
   - Admin CRUD pages.

6. **Build frontend**
   - Base layout with CareerPulse logo.
   - Student dashboard.
   - Job listing and detail pages.
   - Profile and skills pages.
   - Alerts and tracker pages.
   - Admin pages.

7. **Test**
   - Registration/login.
   - Skill matching.
   - Alerts.
   - External apply redirect.
   - Tracker updates.
   - Admin opportunity creation.

8. **Write the final report**
   - Introduction.
   - Problem statement.
   - Objectives.
   - System overview.
   - ER diagram.
   - Normalization.
   - Oracle schema.
   - Sample data.
   - SQL queries and outputs.
   - Flask architecture.
   - Screenshots.
   - Testing.
   - Limitations.
   - Future enhancements.
   - Conclusion.

## 16. Final project pitch

Use this exact pitch in your report, presentation, or demo:

> **CareerPulse is a skill-based internship and job discovery platform for university students. It curates opportunities from official company sources, matches them to each student’s skills, highlights missing skills, sends personalized alerts, and helps students track their application journey. When a student finds a suitable role, CareerPulse directs them to the company’s official application page, ensuring a realistic and transparent job-search workflow.**

## 17. Key phrases to reuse with other LLMs

When asking another LLM for help, start with:

> “I am building CareerPulse, an individual DBMS course project using Oracle Database, Python Flask, HTML, CSS, and JavaScript. It is a skill-based internship and job discovery platform. The admin manually curates real job opportunities with official external apply URLs. Students create skill profiles, receive skill-based job alerts, view match scores and missing skills, open official company application pages, and personally track applications. Companies are database entities only and do not log in. The system does not host applications or make hiring decisions.”

Then ask for the specific piece you need, for example:

- “Create the ER diagram and normalization explanation.”
- “Write the Oracle CREATE TABLE scripts.”
- “Write seed data SQL.”
- “Write the skill-match SQL query.”
- “Create the Flask routes and Jinja templates.”
- “Write the final project report section.”

***

This brief is now your **single source of truth** for CareerPulse. Use it before asking any LLM for schema, SQL, Flask code, frontend pages, testing, or report writing.