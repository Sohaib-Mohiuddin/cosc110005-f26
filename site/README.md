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
| Tools and worksheets | `utilities/` |
| Other course materials | `materials/` (create it when needed) |
| First examples | Root-level `.py` files |

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

Tests verify automatic discovery, future weeks, nested filenames with spaces, safe source highlighting, byte-identical downloads, and every generated internal file/anchor link. GitHub runs these checks on pull requests and before every deployment. The builder never executes the classroom programs.

## GitHub Pages

Repository **Settings → Pages → Build and deployment → Source** must be **GitHub Actions**. The workflow builds on pushes to `main` and publishes with the official Pages actions. Pull requests run checks and build but do not deploy. You can also trigger **Publish course site** manually from Actions. The deployment uses relative links, so it works at the repository's project URL without a custom domain.

## Site files

- `site/course.json`: course details and optional weekly presentation.
- `site/build.py`: discovery, HTML generation, and safe Python/Markdown previews.
- `site/assets/site.css`: responsive layout and colours.
- `site/assets/site.js`: material search, mobile navigation, and copying code.
- `.github/workflows/pages.yml`: validation and publishing.

All materials and navigation work without JavaScript. Search, the mobile menu, and copying code use JavaScript; on small screens with JavaScript disabled, students can still navigate from the overview cards and page breadcrumbs. Fonts have system fallbacks if Google Fonts is unavailable. Python runs on students' computers, not in the browser. Future GUI demonstrations will need a graphical desktop and Tkinter; keep any imported companion files together.
