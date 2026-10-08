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

Include a week and topic in each label to help students find relevant readings. The current collection covers weeks 2–5, with Python documentation, Python for Everybody readings, Python Tutor, and University of Waterloo practice exercises.

Each link automatically displays its website favicon as a small logo. The browser requests icons from Google's favicon service using only the destination hostname (no path, query, or fragment); it sends no referrer. Images load lazily, and the built-in book icon remains visible if a logo is unavailable, blocked, or JavaScript is disabled. No image URLs or API keys need to be maintained in `links.txt`, and site builds do not require network access. These are website logos, rather than article preview images.

The instructor guide remains at `instructor.html`, accessible by entering its address directly. It is no longer linked from student navigation.

## Find course materials

**Search materials** in the sidebar goes to the overview search. Students can combine keywords with a file-type filter or select a type alone, then use **Clear search** to return to browsing. The URL stores the query and file type, allowing searches to be bookmarked or shared and restored with the browser’s Back button. Search controls appear only when JavaScript is available.

## Organize course files

Subfolders are supported. Number demos as `01_topic.py`, `02_topic.py`, etc. New weeks appear automatically when supported files exist. Give a new week a `README.md` beginning with `# Week 6: Your topic` for an automatic title. Optionally add the week to `site/course.json` to customize its title, description, and topic tags. Only weeks with actual files are listed.

Supported types: `.py`, `.md`, `.pdf`, `.txt`, `.csv`, `.json`, `.ipynb`, `.pptx`, `.docx`, `.xlsx`, `.zip`, `.png`, `.jpg`, `.jpeg`, `.svg`, and `.webp`. Python is highlighted without execution; Markdown is rendered; PDFs are embedded with open/download fallbacks. Other files can be downloaded or viewed on GitHub. Search indexes filenames, topics, and textual file contents. Markdown supports headings, paragraphs, lists, tables, fenced/inline code, bold text, and links; HTML is escaped. For advanced notebook or document previews, use the GitHub link.

Only put public student materials into the course folders. All supported files in these folders are published. Hidden files, symlinks, caches, and build folders are excluded. Keep private notes, grades, and unreleased answers out of this public repository.

## Preview and test locally

Python 3.12 or newer is required for the website builder. Student demos keep their own Python requirements. No pip or npm dependencies are required for building the site.

```sh
python -m unittest discover -s site -p 'test_*.py' -v
python site/build.py
python -m http.server 8000 --directory _site
```

On Windows use `py` in place of `python` if needed. Visit <http://localhost:8000>. The builder requires an empty output directory so removed lessons cannot remain in a subsequent deployment. For another local build, delete only the generated `_site` directory or use `python site/build.py --output another-preview` with a fresh directory. Do not commit generated output.

Tests verify automatic discovery, future weeks, nested filenames with spaces, safe source highlighting, byte-identical downloads, course link parsing and rendering, instructor navigation, and every generated internal file/anchor link. GitHub runs these checks on pull requests and before every deployment. The builder never executes the classroom programs.

## GitHub Pages

Repository **Settings → Pages → Build and deployment → Source** must be **GitHub Actions**. The workflow builds on pushes to `main` and publishes with the official Pages actions. Pull requests run checks and build but do not deploy. You can also trigger **Publish course site** manually from Actions. The deployment uses relative links, so it works at the repository's project URL without a custom domain.

## Site files

- `site/course.json`: course details and optional weekly presentation.
- `site/build.py`: discovery, HTML generation, and safe Python/Markdown previews.
- `site/assets/site.css`: responsive layout and colours.
- `site/assets/site.js`: material search, mobile navigation, and copying code.
- `.github/workflows/pages.yml`: validation and publishing.

All materials and navigation work without JavaScript. Search, the mobile menu, and copying code use JavaScript; on small screens with JavaScript disabled, students can still navigate from the overview cards and page breadcrumbs. Fonts have system fallbacks if Google Fonts is unavailable. Python runs on students' computers, not in the browser. Future GUI demonstrations will need a graphical desktop and Tkinter; keep any imported companion files together.
