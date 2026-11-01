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
