# CareerPulse visual evidence
These are actual Chromium captures, except the ERD, which is rendered from Graphviz.
Images show each milestone at the time it was tested; later milestones add navigation.

| Feature | Desktop | Mobile |
| --- | --- | --- |
| Saved jobs | [Screenshot](screenshots/saved-desktop.png) | [Screenshot](screenshots/saved-mobile.png) |
| Manual tracker | [Screenshot](screenshots/tracker-desktop.png) | [Screenshot](screenshots/tracker-mobile.png) |
| Job alerts | [Screenshot](screenshots/alerts-desktop.png) | [Screenshot](screenshots/alerts-mobile.png) |
| Notifications | [Screenshot](screenshots/notifications-desktop.png) | [Screenshot](screenshots/notifications-mobile.png) |
| Authentication | [Screenshot](screenshots/auth-desktop.png) | [Screenshot](screenshots/auth-mobile.png) |
| Admin catalog | [Screenshot](screenshots/admin-desktop.png) | [Screenshot](screenshots/admin-mobile.png) |
| Expanded discovery | [Screenshot](screenshots/explore-desktop.png) | [Screenshot](screenshots/explore-mobile.png) |
| Oracle design | [ERD](screenshots/oracle-erd.png) | — |

Full-page phone captures show the fixed navigation at the viewport's bottom position;
it stays anchored to the phone screen while the content scrolls.

## Final end-to-end journey
- [Updated student dashboard](screenshots/journey-dashboard-desktop.png) · [Mobile](screenshots/journey-dashboard-mobile.png)
- [Confirmed application tracker](screenshots/journey-tracker-desktop.png) · [Mobile](screenshots/journey-tracker-mobile.png)
- [Admin-created opportunity](screenshots/journey-admin-catalog-desktop.png) · [Mobile](screenshots/journey-admin-catalog-mobile.png)
- [Updated admin overview](screenshots/journey-admin-desktop.png) · [Mobile](screenshots/journey-admin-mobile.png)

## Authentication entry fix
- [Homepage access buttons](screenshots/auth-entry-desktop.png) · [Mobile](screenshots/auth-entry-mobile.png)
- [Login](screenshots/auth-login-1440.png) · [Mobile](screenshots/auth-login-390.png)
- [Registration](screenshots/auth-register-1440.png) · [Mobile](screenshots/auth-register-390.png)

## Glass authentication

- [Sign in — desktop](screenshots/glass-login-1440.png)
- [Sign in — mobile](screenshots/glass-login-390.png)
- [Registration — desktop](screenshots/glass-register-1440.png)
- [Registration — mobile](screenshots/glass-register-390.png)

## Transparent authentication logo and handwritten concept

The original SVG is unchanged. The authentication logo now sits without a white tile on a light top header so its navy lettering remains readable. Registration uses a slightly larger logo.

- [Current registration — desktop](screenshots/transparent-logo-register-1440.png)
- [Current registration — mobile](screenshots/transparent-logo-register-390.png)
- [Handwritten concept — desktop](screenshots/handwritten-register-preview-1440.png)
- [Handwritten concept — mobile](screenshots/handwritten-register-preview-390.png)

The handwritten concept is a browser screenshot with a temporary Caveat font override, not the live heading style. Font source: [Google Fonts Caveat](https://github.com/google/fonts/tree/main/ofl/caveat). The live page retains the bold heading pending selection.

Validation: 35 unit tests and the full Chromium workflow passed. Current and concept layouts passed overflow checks at 320, 390, 768 and 1440px; desktop/mobile concept screenshots were visually inspected.
