# Shared workspace loading

CareerPulse keeps Flask routes and Jinja-rendered HTML as its data source. With
JavaScript enabled, student workspace navigation, search/filter forms and supported
mutations fetch those same routes, including their existing CSRF protection and
303 redirects. Public, authentication, admin and external-apply flows retain normal
browser navigation. Without JavaScript, every page and form still works normally.

Initial server-rendered content is ready when it arrives, so it is displayed
immediately. There is no artificial loading delay, duplicate initial data request,
or fake zero value. Skeletons appear during real pending workspace requests and
crossfade into the response's data. Actual zero counts remain legitimate data.

## Contract

- `data-load-region` marks a group of independently loaded content. Its immediate
  children are the staggered items. Nested regions are skipped by the outer group.
- `static/js/loading.js` exposes `CareerPulseLoading.begin(root)`, `clear(states)`
  and `reveal(root)` for future section-level fetches.
- Skeletons use actual text/field geometry, including the width of each number,
  and preserve card dimensions, borders and corner radii. Pending fields are inert
  and their group has `aria-busy=true`; loading/failure feedback uses a live region.
- All timing lives in `static/css/loading.css`: 230ms, a shared ease-out curve,
  6px upward entrance, and 70ms stagger. Short-list delay caps at 350ms (580ms
  settling); long-list delay caps at 700ms (930ms settling). These budgets begin
  when the response arrives: network latency is outside the animation budget.
- Placeholder gray is `--surface-1: #e5e9ee`. There is no shimmer or content spinner.
- Reduced motion makes the swap immediate. Responsive resizing ends current
  entrances and remeasures pending skeletons; overlays cannot overflow the page.
- New GET requests supersede old GETs. Writes are not retried or interrupted by
  another enhanced action. Failures restore content and entered values; uncertain
  writes tell the user to check before submitting again. Requests time out at 30s.
- Browser back/forward, response titles, active navigation and main-content focus
  update with successful navigation. Validation errors retain the canonical URL.

All UI icons use the pinned Lucide 0.468.0 outline paths in `templates/icons.html`.
The helper emits inline SVG with width/height attributes and CSS sizing. Separate
icon image requests and character/emoji icons have been removed. Original brand
artwork and decorative auth underlines are preserved; they are not UI icon packs.
The Lucide license remains in `static/icons/LICENSE`.

## Dashboard data

Overview, recommended roles, closing-soon jobs, tracker counts, alerts and skills
use existing repository/profile/activity data. Closing-soon means zero through
seven days remaining. The upcoming-events panel is an honest empty state because
this project has no event scheduler; application notes remain available in Tracker.

## Verification (Windows PowerShell)

From the repository directory with development requirements installed:

```powershell
.\.venv\Scripts\python.exe app.py
# In another terminal:
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe tests/browser_loading.py
.\.venv\Scripts\python.exe tests/browser_sidebar.py
.\.venv\Scripts\python.exe tests/browser_landing.py
.\.venv\Scripts\python.exe tests/browser_smoke.py
```

The browser scripts launch isolated local Flask instances. Screenshots are written
to ignored `artifacts/dashboard/`, `artifacts/sidebar/`, `artifacts/landing/` and
`artifacts/browser/`. Tests use Chromium responsive emulation, not physical devices.


## Discovery search

Explore keeps its search header visible and debounces typing by 300ms, including
composition-input support. Search and Apply filters fetch the existing Flask
route and replace only `#discovery-results`; inputs and typing focus stay intact.
The result region uses the same skeleton and entrance utilities as other pages.
Search matches title, company and required/preferred skill tags. Filters combine
with AND logic, while best-match scoring continues to use required skills only.

Successful live searches replace the current URL; Apply and Reset create history
entries. Query parameters restore all filter selections on reload and Back/Forward.
Reset clears search and every filter. New input cancels obsolete requests, and a
failed request restores existing results. Without JavaScript, Search and Apply
remain normal GET forms. Result counts are announced through the shared live region.
