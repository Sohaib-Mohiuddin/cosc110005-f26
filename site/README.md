# Course website maintenance

The student site is published at <https://sohaib-mohiuddin.github.io/cosc110005-f26/>.

## Add materials without editing the website

1. Open a course folder on GitHub, choose **Add file → Upload files** (or **Create new file**), and add your material.
2. Commit to `main`, or create and merge a pull request.
3. Wait for **Actions → Publish course site** to turn green. Refresh the site after deployment.

You can also add files locally, commit, and push as usual. The build reads the latest files directly; do not copy course code into the site folder.

| Content | Location |
| --- | --- |
| Weekly demonstrations, companion files, notes | `week-N-demos/` |
| Exercise handouts and starter code | `in-class-exercise-N/` |
| Midterm practice exercises and study guide | `Midterm Preparation/` |
| Tools and worksheets | `utilities/` |
| Other course materials | `materials/` (create it when needed) |
| First examples | Root-level `.py` files |
| Shared websites and references | Root-level `links.txt` |

## Share course links

Add one entry per line to `links.txt`, then commit and push. The **Course links** page reads this file automatically and is accessible from the sidebar and overview. Supported formats:

```text
https://docs.python.org/3/
Python tutorial | https://docs.python.org/3/tutorial/
[Python downloads](https://www.python.org/downloads/)
```

Blank lines and lines beginning with `#` are ignored. Labels are optional; a plain URL displays its host as the title. Links keep their file order, and duplicate URLs appear only once. Use complete `http://` or `https://` URLs without spaces or embedded credentials. Invalid entries fail the build with the filename and line number so a typo can be corrected before publishing. An empty or missing file displays a friendly empty state. Links work without JavaScript and open in the same tab.

Include a week and topic in each label to help students find relevant readings. The current collection covers weeks 2–5, with Python documentation, Python for Everybody readings, Python Tutor, University of Waterloo practice exercises, and GeeksforGeeks readings for individual concepts, including pseudocode and flowcharts.

Each link displays a single image: its website favicon, or a local book icon if the logo is unavailable, blocked, or JavaScript is disabled. There is no additional arrow or overlapping fallback icon. The browser requests icons from Google's favicon service using only the destination hostname (no path, query, or fragment); it sends no referrer. Images load lazily. No image URLs or API keys need to be maintained in `links.txt`, and site builds do not require network access. These are website logos, rather than article preview images.

The instructor guide remains at `instructor.html`, accessible by entering its address directly. It is no longer linked from student navigation.

## Find course materials

**Search materials** in the sidebar goes to the overview search. Students can combine keywords, file type, and week (or Resources), then use **Clear search** to return to browsing. Matching text excerpts explain search results. The URL stores `q`, `type`, and `week`, so searches can be bookmarked, shared, and restored on return. Search controls appear only when JavaScript is available.

## Organize course files

Subfolders are supported. Number demos as `01_topic.py`, `02_topic.py`, etc. New weeks appear automatically when supported files exist. Give a new week a `README.md` beginning with `# Week 6: Your topic` for an automatic title. Optionally add the week to `site/course.json` to customize its title, description, and topic tags. Only weeks with released files are listed. In a Git checkout, discovery includes only Git-tracked course files. Keep future weeks untracked locally and add/commit/push each week when ready, as before. This same released-material list drives pages, search, runtime file manifests, and ZIP bundles. A source ZIP without `.git` treats its included course files as released.

Supported types: `.py`, `.md`, `.pdf`, `.txt`, `.csv`, `.json`, `.ipynb`, `.pptx`, `.docx`, `.xlsx`, `.zip`, `.png`, `.jpg`, `.jpeg`, `.svg`, and `.webp`. Python has a highlighted source view and, for compatible console examples, an optional browser editor and runner; Markdown is rendered; PDFs are embedded with open/download fallbacks. Other files can be downloaded or viewed on GitHub. Search indexes filenames, topics, and textual file contents, and shows highlighted excerpts for matching text. Markdown supports headings, paragraphs, lists, tables, fenced/inline code, bold text, and links; HTML is escaped. For advanced notebook or document previews, use the GitHub link.

Only put public student materials into tracked course folders. All supported tracked files in these folders are published. Hidden files, symlinks, caches, and build folders are excluded. Keep private notes, grades, and unreleased answers out of this public repository.

## Preview and test locally

Python 3.12 or newer is required for the website builder. Student demos keep their own Python requirements. No pip or npm dependencies are required for building the site.

```sh
python -m unittest discover -s site -p 'test_*.py' -v
python site/build.py
python -m http.server 8000 --directory _site
```

On Windows use `py` in place of `python` if needed. Visit <http://localhost:8000>. The builder requires an empty output directory so removed lessons cannot remain in a subsequent deployment. For another local build, delete only the generated `_site` directory or use `python site/build.py --output another-preview` with a fresh directory. Do not commit generated output.

Python tests verify discovery, exclusion of untracked weeks, dependency bundles, practice manifests, safe previews, byte-identical downloads, course links, and every generated internal file/anchor link. Browser checks run real Python and verify search, input, output/error handling, Stop, time/output limits, practice checks, saved work, mobile layout, keyboard navigation, and no-JavaScript/storage fallbacks. GitHub runs both suites on pull requests and before deployment. The builder itself never executes classroom programs.

## GitHub Pages

Repository **Settings → Pages → Build and deployment → Source** must be **GitHub Actions**. The workflow builds on pushes to `main` and publishes with the official Pages actions. Pull requests run checks and build but do not deploy. You can also trigger **Publish course site** manually from Actions. The deployment uses relative links, so it works at the repository's project URL without a custom domain.

## Site files

- `site/course.json`: course details and optional weekly presentation.
- `site/build.py`: discovery, HTML generation, and safe Python/Markdown previews.
- `site/assets/site.css`: responsive layout and colours.
- `site/assets/site.js`: search, navigation, reading settings, progress, and copying code.
- `site/learning.py`: released-file bundles, dependency discovery, and practice markup.
- `site/practice_cases.json`: public sample checks for the 20 midterm starters.
- `site/assets/runner.js`, `python-worker.mjs`: browser editor and isolated runs.
- `site/browser-tests/`: pinned Playwright tools and student-flow checks.
- `.github/workflows/pages.yml`: validation and publishing.

All materials and navigation work without JavaScript. Search, the mobile menu, and copying code use JavaScript; on small screens with JavaScript disabled, students can still navigate from the overview cards and page breadcrumbs. Fonts have system fallbacks if Google Fonts is unavailable. Compatible Python examples run on the student’s device through Pyodide in a Web Worker. GUI demonstrations still need desktop Python and Tkinter. Download complete lesson ZIPs to keep companion files together.


## Browser practice

Compatible Python pages offer **Try Python in your browser**. The editor starts from the original file; edits never modify course source files. The runtime is pinned to Pyodide `314.0.7` and fetched from jsDelivr only on Run or Run sample checks. An initial connection is required. Runtime upgrades should update the pinned URL in `python-worker.mjs` and pass the browser suite.

Enter all `input()` answers before running, one per line. A trailing newline terminates the last answer; a blank line represents an empty answer. Include sentinels such as `done` or `0` when the program expects one. Missing answers show the Python EOF error and a hint. Interactive prompting during a run is not currently supported.

Each run or check gets a fresh worker and Python environment. Stop terminates that worker; runs also stop after 10 seconds or 64 KB of output. Runtime/file loading has a separate 60-second limit. A worker keeps loops off the interface thread; it is not a security boundary for arbitrary hostile code. Student Python has the browser capabilities exposed by Pyodide. Output is rendered as text, never HTML.

Same-folder Python/text/CSV/JSON files and identifiable imported course modules are loaded from the released-material manifest. Files retain their repository paths, `__file__` is set, and execution starts in the selected file’s directory. Files created during a run are temporary. Dynamic imports, third-party packages, networking, and desktop/system APIs may need additional support; use desktop Python for those cases. Tkinter, turtle, subprocess, multiprocessing, socket, and ctypes imports (including imported course dependencies) display **Requires desktop Python**.

**Reset code** asks before discarding edits. **Download my code** saves the edited `.py` file; lesson ZIPs contain the instructor’s original files. Edits, program input, reading settings, and self-marked completion are stored in `localStorage`, scoped to this course URL. They do not sync or submit to the instructor and can disappear when browser data is cleared. If storage is blocked/full, the editor still works and reports that saving failed. Download important work.

## Practice checks

`utilities/demo_cases.json` supplies existing console smoke checks. `site/practice_cases.json` supplies public midterm checks. Only a displayed, released program’s cases enter its runner page. The browser runs the student’s current editor contents and compares actual output with the case’s `contains` fragments. Errors and execution limits fail that case. Results include actual output for review. Checks are not grading or exhaustive algorithm verification; students still review requirements, trace code, and add their own cases.

A case has `label`, `stdin`, and nonempty `contains` strings. Optional `overrides` temporarily substitute named top-level assignments using Python’s AST for exercises with hardcoded input variables. Those changes are displayed in the sample-case panel and do not change the editor or saved file. Missing assignments produce an explicit error. Sample data and expected output are intentionally public; do not store private tests or solutions here.

## Weekly navigation, progress, and lesson bundles

The overview’s **This week** shortcut defaults to the highest released week. Set optional `current_week` in `site/course.json` to feature a different released week; an unavailable value falls back to the latest released week. Each week can specify an `objectives` list alongside its title, description, and tags. Weeks without custom objectives receive general prediction, experimentation, and tracing goals.

Opening a Python example updates **Resume** on the overview. Students can mark examples as practised; completion is self-reported and stored locally. Code size and line wrapping settings apply to both source and editor. Tab leaves the editor normally; Ctrl+Enter / Command+Enter runs code.

**Download complete lesson ZIP** includes that course folder’s released files plus identifiable imported course modules, preserving folders and providing `RUN_LESSON.txt`. These archives are generated during each build and never include untracked weeks by default.

## Browser checks and private previews

The HTML build still requires only Python 3.12+. Browser verification additionally requires Node 24, Playwright/Chromium, and network access to the pinned Pyodide CDN:

```sh
python site/build.py
cd site/browser-tests
npm ci
npx playwright install chromium
npm test
```

The test script starts and stops its own localhost-only server under a GitHub Pages-style project path. On Linux CI, use `npx playwright install --with-deps chromium`. Optional `SITE_OUTPUT` selects an existing generated site; `SITE_BASE_URL` selects an already running preview. `SCREENSHOT_DIR` saves desktop/mobile screenshots.

For an explicitly private preview of unreleased local material, use a fresh output directory:

```sh
python site/build.py --include-untracked --output /tmp/private-course-preview
```

Never deploy that private preview. The GitHub workflow uses the default tracked-only build.
