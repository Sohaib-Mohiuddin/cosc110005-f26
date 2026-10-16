# Navigation delivery plan

Base: the published student studio on main. Preserve all course content and browser saves. Publish only released material; weeks 8–14 remain untracked.

Use short vertical slices with explicit acceptance gates, then complete integration before publishing main.

| Sprint | Deliverable | Acceptance gate | Status |
| --- | --- | --- | --- |
| 1 | Five primary sections and contextual sidebars | Correct section on direct links; exact page selection; released-content-only links | Complete |
| 2 | Desktop reading space and dedicated tool panels | Sidebar collapse persists; workspace file and practice activity panels remain usable | Complete |
| 3 | Mobile drawer and compact selectors | Focus containment, Escape/backdrop close, file/activity switching, no horizontal overflow at 320–1440 px | Complete |
| 4 | Regression and delivery | Generator/link tests, navigation and Python browser suites, main publication, CI and live route checks | All local gates complete; publication tracked in Actions |

The global menu is Course, Assignments, Practice, Workspace, and My Study. Keep Reference and Display as utilities. Primary selection identifies a section; only an exact contextual destination identifies the current page. Preserve breadcrumbs and original/readable assignment links.

Automated gates are `python3 -m unittest discover -s site -p 'test_*.py'` and `npm test --prefix site/browser-tests` after a fresh default build. Existing generator checks verify every generated local URL and fragment. Navigation-specific checks cover untracked future-content exclusion, deep-link selection, responsive width, keyboard focus, persistence, and editor/selector continuity. Existing runtime and disconnected-browser suites remain part of the release gate.

CI and live verification are recorded in the final delivery message after main publication; do not mark those gates complete before observing their results.

## Acceptance evidence

- All 24 Python checks pass, including generated local URLs/fragments, exact context selection, and a tracked-only fixture excluding future weeks and assignments.
- Real Chromium checks pass section changes, original/readable assignment briefs, lesson deep links, study queue/bookmark filters, practice topic markers, persistent sidebar collapse, and workspace/practice panels.
- Layouts at 1440, 1024, 800, 390, and 320 px have no horizontal page overflow. The mobile drawer receives initial focus, contains forward/reverse Tab navigation, closes with Escape or its backdrop, and restores focus. Resizing an open drawer preserves usable focus.
- Compact activity/file selectors retain selection and editor changes; the normal editor Tab behavior remains available. With JavaScript disabled, the visible primary and contextual links still reach assignment instructions on mobile.
- Verification found and corrected client-side exact-page selection, topic-anchor synchronization, and the drawer visibility transition that prevented initial keyboard focus. The fresh navigation candidate passes all of these regressions.
- The final immutable build passes all three browser suites: navigation acceptance, the original student workflow regressions, and studio acceptance. Real Python execution, assignment/PDF/ZIP flows, saved edits, practice checks, portable backup recovery, reduced motion, and disconnected lesson/project execution remain working.
- CI exposed a browser-ordering race when a resized layout hides the focused navigation control before the media callback. The fix retains focus ownership during that transition and clears it on ordinary blur. Extra checks cover repeated crossings, sidebar links/toggles, mobile Menu recovery, and preserving editor focus. All three suites also pass using CI’s Chromium headless-shell executable; the deployment gate remains required.
