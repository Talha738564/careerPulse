# Header, navigation and authentication layout validation

Implemented a navy/blue/teal header with original logo assets, account actions and
notification bell, followed by introductory text and a unified glass search bar.
The search uses a shared focus outline, preserves its query after submission and
keeps its button visible at narrow widths. SVG outline icons replace text glyphs.
Mobile/tablet navigation floats in a frosted pill with safe-area spacing; desktop
retains the workspace sidebar with matching icons and translucent active state.
Authentication forms use compact desktop spacing without fixed heights or clipped
validation content. Small screens retain natural vertical scrolling.

Verification on 2026-11-02:
- 35 Python service/route tests passed.
- Chromium student/admin workflow passed, with no browser JavaScript errors.
- 64 combinations: eight routes at 320, 390, 768, 1024, 1280, 1366, 1440 and
  1920px widths; no horizontal page overflow.
- Login and registration fit tested desktop heights from 720px upward.
- Search query submission, retained query and shared focus outline passed.
- Reviewed rendered mobile dashboard and laptop registration screenshots.

Regression checks are included in `tests/browser_smoke.py`. Run in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe tests/browser_smoke.py
```

Validation messages, browser zoom, smaller heights and mobile keyboards may require
natural scrolling so all form controls remain accessible.
