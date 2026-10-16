# Student platform delivery plan

Initial release base: 4829e85. During development, 501bb9a released the fifth week 7 demo. The current released files are the only course-material source; weeks 8–14 stay private.

## Delivery method

Use short vertical slices with acceptance criteria, a working increment, targeted verification, and a recorded review. Complete the release gate before updating main. Preserve original course files and existing student saves. The eight priority features and five complementary features form the release scope; notebook integration remains a later option.

| Sprint | Scope | Acceptance gate | Status |
| --- | --- | --- | --- |
| 0 | Inventory, release boundary, acceptance plan | Existing tests pass; released file list recorded | Complete |
| 1 | Design system, shared state, accessible editor and runtime | Responsive shell; motion/display controls; real Python contract tests | Complete |
| 2 | Multi-file workspace, checks, errors, trace replay | Import/edit/run/export; strict comparisons; bounded trace and useful errors | Complete |
| 3 | Guided practice, concepts, reference, study queue and backups | Four activity types; prerequisites; portable restore; notes and bookmarks | Complete |
| 4 | Readable assignment, what's new, offline packs | Faithful readable brief; only released files; explicit offline availability | Complete |
| 5 | Integration, regression review, main publication | Python/JS/browser checks; mobile/reduced-motion/storage/offline tests; live verification | Local gates complete; publication tracked in Actions |

## Definition of done

- Student tasks work with keyboard and mobile layouts; moving decoration has pause and reduced-motion support.
- Projects, notes, progress and preferences can be exported/restored without exposing unrelated browser storage.
- New learning activities use original practice examples rather than assignment solutions.
- Python execution remains in a worker with Stop, timeout and output limits. Trace replay and check modes state their limits.
- Offline packs list what was saved and explain when Python runtime files still need downloading.
- Every generated local link resolves. Untracked course files are absent from pages, manifests, packs and ZIPs.
- Existing lesson, assignment, search and runner flows keep working.
- All intended files reach main, CI succeeds, and live pages are verified.

## Sprint review evidence

Record completed gates and any material implementation limits here as work progresses.

- Sprint 0: 17 Python tests pass. Release inventory updated to include the externally committed week 7 demo (501bb9a).
- Sprint 1: shared engine/editor/storage and design shell compile; browser probe runs real Python, captures/replays a 10-step trace, opens reference, and checks a prediction. Existing generator/link tests pass.

- Sprint 2: browser gate passes multi-file imports, companion/data execution, generated downloads, strict output modes, value assertions, syntax-only checks, error navigation, bounded trace replay, ZIP integrity and project snapshots.

- Sprint 3: acceptance suite passes all four practice formats, progressive explanations, prerequisites/reference, study notes/queue/bookmarks, backup restoration into a new browser, invalid-key rejection and quota rollback.
- Sprint 4: readable brief checked against PDF example images; disconnected browser tests read a selected pack and execute both a lesson and a workspace project. Unsaved reading URLs show the offline fallback.
- Sprint 5: 21 Python tests pass, JavaScript syntax checks pass, and the original browser regression suite passes with the shared runtime. The final studio acceptance build also passes confirmed project removal, numeric expectation validation, UTF-8 ZIP filenames, actual cache-marker availability, display persistence, backup recovery, mobile/reduced-motion behavior, and disconnected lesson/project execution.

The final delivery gate is the [Publish course site workflow](https://github.com/Sohaib-Mohiuddin/cosc110005-f26/actions/workflows/pages.yml), followed by checks of the deployed routes and a real browser Python run. Deployment and live-verification evidence is recorded in the release delivery message after publication; this source record describes the gates completed before publication.
