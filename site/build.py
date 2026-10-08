"""Build the course library with Python's standard library. No course code is executed."""
from __future__ import annotations

import argparse
import html
import io
import json
import keyword
import posixpath
import re
import shutil
import tokenize
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SUPPORTED = {'.py', '.md', '.pdf', '.txt', '.csv', '.json', '.ipynb', '.pptx', '.docx', '.xlsx', '.zip', '.png', '.jpg', '.jpeg', '.svg', '.webp'}
EXCLUDED = {'__pycache__', 'node_modules', '.venv', 'venv', '_site', 'site', 'tests'}
ICONS = {
    'grid': '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    'book': '<path d="M12 6c-3-3-7-3-10-2v15c3-1 7-1 10 2 3-3 7-3 10-2V4c-3-1-7-1-10 2Zm0 0v15"/>',
    'code': '<path d="m8 5-6 7 6 7m8-14 6 7-6 7m-3-17-2 20"/>',
    'file': '<path d="M14 2H5v20h14V7Zm0 0v6h5M8 12h8m-8 4h6"/>',
    'arrow': '<path d="M5 12h14m-6-6 6 6-6 6"/>',
    'search': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
    'menu': '<path d="M4 6h16M4 12h16M4 18h16"/>',
    'branch': '<circle cx="6" cy="4" r="2"/><circle cx="6" cy="20" r="2"/><circle cx="18" cy="5" r="2"/><path d="M6 6v12m0-5h6a6 6 0 0 0 6-6"/>',
}


def esc(value):
    return html.escape(str(value), quote=True)


def icon(name):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'


def link_logo(url):
    """Let the browser load a favicon using only the public link's hostname."""
    hostname = quote(urlsplit(url).hostname, safe='')
    source = f'https://www.google.com/s2/favicons?domain={hostname}&sz=64'
    return ('<span class="resource-icon course-link-logo" aria-hidden="true">'
            f'<img src="assets/link-fallback.svg" data-logo-src="{esc(source)}" alt="" width="32" height="32" '
            'loading="lazy" decoding="async" referrerpolicy="no-referrer"></span>')


def natural(value):
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r'(\d+)', str(value))]


def title_for(path):
    if path.name.lower() == 'readme.md':
        return 'Folder guide'
    return re.sub(r'^\d+[_-]?', '', path.stem).replace('_', ' ').replace('-', ' ').capitalize()


def read_links(path):
    """Read public course links without fetching them; report malformed lines early."""
    if not path.exists():
        return []
    links, seen = [], set()
    for number, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        markdown = re.fullmatch(r'\[([^\]]+)\]\((.+)\)', line)
        if markdown:
            label, url = markdown.groups()
        elif '|' in line:
            label, url = line.split('|', 1)
        else:
            label, url = '', line
        label, url = label.strip(), url.strip()
        try:
            parts = urlsplit(url)
            valid = (parts.scheme in {'http', 'https'} and parts.hostname
                     and not parts.username and not parts.password
                     and not re.search(r'[\s\x00-\x1f\x7f\\]', url))
            parts.port  # Validate the port as well as the host.
        except ValueError:
            valid = False
        if not valid:
            raise ValueError(f'{path.name}:{number}: expected an http(s) URL, Label | URL, or [Label](URL)')
        if url not in seen:
            links.append({'title': label or parts.netloc, 'url': url})
            seen.add(url)
    return links


def discover(root):
    """Only publish course folders and root Python examples; ignore hidden/private build files."""
    files = []
    candidates = list(root.glob('*.py'))
    for folder in root.iterdir():
        if folder.is_dir() and (re.fullmatch(r'week-\d+-demos', folder.name) or re.fullmatch(r'in-class-exercise-\d+', folder.name) or folder.name in {'utilities', 'materials', 'Midterm Preparation'}):
            candidates.extend(folder.rglob('*'))
    for path in sorted(candidates, key=lambda p: natural(p.relative_to(root).as_posix())):
        relative = path.relative_to(root)
        if not path.is_file() or path.is_symlink() or path.suffix.lower() not in SUPPORTED:
            continue
        if any(part.startswith('.') or part in EXCLUDED for part in relative.parts):
            continue
        # Do not follow a symlinked parent into unrelated local files.
        if any(parent.is_symlink() for parent in path.parents if parent != root and root in parent.parents):
            continue
        if not path.resolve().is_relative_to(root.resolve()):
            continue
        text = path.read_text(encoding='utf-8-sig', errors='replace') if path.suffix.lower() in {'.py', '.md', '.txt', '.csv', '.json'} else ''
        week = re.match(r'week-(\d+)-demos/', relative.as_posix())
        files.append({'path': relative.as_posix(), 'title': title_for(path), 'kind': path.suffix[1:].upper(), 'week': int(week[1]) if week else None, 'text': text, 'url': 'view/' + quote(relative.as_posix(), safe='/') + '.html'})
    return files


def highlight_python(source):
    """Tokenize rather than execute; preserve original source and escape all HTML."""
    offsets = [0]
    for line in source.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))
    def offset(position):
        row, col = position
        return offsets[min(row - 1, len(offsets) - 1)] + col
    tokens = []
    try:
        for token in tokenize.generate_tokens(io.StringIO(source).readline):
            style = {tokenize.COMMENT: 'comment', tokenize.STRING: 'string', tokenize.NUMBER: 'number'}.get(token.type)
            if token.type == tokenize.NAME and keyword.iskeyword(token.string):
                style = 'keyword'
            if style:
                tokens.append((offset(token.start), offset(token.end), style))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        pass  # In-progress classroom examples should still be readable.
    chunks, position = [], 0
    for start, end, style in tokens:
        if start < position:
            continue
        chunks.append(esc(source[position:start]))
        chunks.append('\n'.join(f'<span class="tok-{style}">{esc(line)}</span>' for line in source[start:end].split('\n')))
        position = end
    chunks.append(esc(source[position:]))
    return '\n'.join(f'<span class="code-line">{line}</span>' for line in ''.join(chunks).split('\n'))


class Site:
    def __init__(self, root, out):
        self.root, self.out = root, out
        self.config = json.loads((root / 'site/course.json').read_text(encoding='utf-8'))
        self.course_links = read_links(root / 'links.txt')
        self.files = discover(root)
        self.by_path = {item['path']: item for item in self.files}
        self.weeks = sorted({item['week'] for item in self.files if item['week'] is not None})

    def week_info(self, week):
        info = self.config.get('weeks', {}).get(str(week), {})
        guide = self.by_path.get(f'week-{week}-demos/README.md', {}).get('text', '')
        heading = re.search(r'^#\s+(?:Week\s+\d+:?\s*)?(.+)', guide, re.M | re.I)
        return {'title': info.get('title', heading[1] if heading else f'Week {week} materials'), 'description': info.get('description', 'Explore this week’s code examples, notes, and practice materials.'), 'tags': info.get('tags', ['Python', 'Practice'])}

    def github(self, path='', mode='blob'):
        return self.config['repository'].rstrip('/') + '/' + mode + '/' + quote(self.config['branch'], safe='') + ('/' + quote(path, safe='/') if path else '')

    def link(self, target, current):
        return quote(posixpath.relpath(unquote(target), posixpath.dirname(current) or '.'), safe='/')

    def row(self, item, current):
        return f'<a class="file-row" href="{self.link(item["url"], current)}"><span class="file-kind">{esc(item["kind"])}</span><div><strong>{esc(item["title"])}</strong><small>{esc(item["path"])}</small></div><span class="arrow">{icon("arrow")}</span></a>'

    def markdown(self, text, source, current):
        """Small, safe Markdown subset used by course guides: headings, lists, tables, links, code."""
        def resolve(href):
            parts = urlsplit(href)
            if parts.scheme:
                return href if parts.scheme in {'http', 'https', 'mailto'} else '#'
            if parts.netloc:
                return '#'
            path = posixpath.normpath(posixpath.join(posixpath.dirname(source), unquote(parts.path)))
            if path in self.by_path:
                return self.link(self.by_path[path]['url'], current)
            week = re.fullmatch(r'week-(\d+)-demos/?', path)
            if week and int(week[1]) in self.weeks:
                return self.link(f'weeks/week-{week[1]}.html', current)
            return self.github(path)

        def inline(line):
            pattern = r'(`[^`]+`|\[[^\]]+\]\([^)]+\)|\*\*[^*]+\*\*)'
            result = []
            for part in re.split(pattern, line):
                if part.startswith('`') and part.endswith('`'):
                    result.append('<code>' + esc(part[1:-1]) + '</code>')
                elif part.startswith('[') and re.fullmatch(r'\[([^\]]+)\]\(([^)]+)\)', part):
                    match = re.fullmatch(r'\[([^\]]+)\]\(([^)]+)\)', part)
                    result.append(f'<a href="{esc(resolve(match[2]))}">{esc(match[1])}</a>')
                elif part.startswith('**') and part.endswith('**'):
                    result.append('<strong>' + esc(part[2:-2]) + '</strong>')
                else:
                    result.append(esc(part))
            return ''.join(result)

        lines, rendered, index = text.splitlines(), [], 0
        while index < len(lines):
            line = lines[index]
            if not line.strip():
                index += 1
                continue
            if line.startswith('```'):
                code = []
                index += 1
                while index < len(lines) and not lines[index].startswith('```'):
                    code.append(lines[index]); index += 1
                rendered.append('<pre><code>' + esc('\n'.join(code)) + '</code></pre>')
            elif line.startswith('#') and re.match(r'#{1,6}\s', line):
                level = len(line) - len(line.lstrip('#'))
                rendered.append(f'<h{level}>' + inline(line[level:].strip()) + f'</h{level}>')
            elif line.startswith('|'):
                rows = []
                while index < len(lines) and lines[index].startswith('|'):
                    cells = lines[index].strip().strip('|').split('|')
                    if not all(re.fullmatch(r'\s*:?-+:?\s*', cell) for cell in cells):
                        tag = 'th' if not rows else 'td'
                        rows.append('<tr>' + ''.join(f'<{tag}>' + inline(cell.strip()) + f'</{tag}>' for cell in cells) + '</tr>')
                    index += 1
                rendered.append('<div class="table-scroll"><table>' + ''.join(rows) + '</table></div>')
                continue
            elif re.match(r'\s*(?:[-*]|\d+\.)\s', line):
                ordered = bool(re.match(r'\s*\d+\.', line))
                tag, items = ('ol' if ordered else 'ul'), []
                pattern = r'\s*\d+\.\s+' if ordered else r'\s*[-*]\s+'
                while index < len(lines) and re.match(pattern, lines[index]):
                    items.append('<li>' + inline(re.sub(pattern, '', lines[index], count=1)) + '</li>'); index += 1
                rendered.append(f'<{tag}>' + ''.join(items) + f'</{tag}>')
                continue
            else:
                paragraph = [line]
                index += 1
                while index < len(lines) and lines[index].strip() and not re.match(r'^(?:#|```|\||[-*]\s|\d+\.\s)', lines[index]):
                    paragraph.append(lines[index]); index += 1
                rendered.append('<p>' + inline(' '.join(paragraph)) + '</p>')
                continue
            index += 1
        return ''.join(rendered)

    def write(self, current, title, body, active='overview'):
        prefix = posixpath.relpath('.', posixpath.dirname(current) or '.') + '/'
        def nav(target, label, symbol, key):
            selected = active == key
            return f'<a class="nav-link{" active" if selected else ""}" href="{self.link(target, current)}"{chr(32) + "aria-current=\"page\"" if selected else ""}>{symbol}{label}</a>'
        menu = nav('index.html', 'Course overview', icon('grid'), 'overview') + nav('getting-started.html', 'Getting started', icon('code'), 'start') + nav('resources.html', 'Exercises & resources', icon('file'), 'resources') + nav('links.html', 'Course links', icon('book'), 'links')
        if 'Midterm Preparation/README.md' in self.by_path:
            menu += nav(self.by_path['Midterm Preparation/README.md']['url'], 'Midterm preparation', icon('book'), 'midterm')
        menu += f'<a class="nav-link" href="{prefix}index.html#weekly-materials">{icon("search")}Search materials</a>'
        weekly = ''.join(nav(f'weeks/week-{week}.html', f'Week {week:02d}', f'<span class="week-dot">{week:02d}</span>', f'week-{week}') for week in self.weeks)
        page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Python demonstrations, weekly materials, and practice for {esc(self.config['code'])}. Read the code, try it yourself, and learn one step at a time."><meta name="theme-color" content="#23674b"><title>{esc(title)} · {esc(self.config['code'])}</title><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/site.css"><script src="{prefix}assets/site.js" defer></script></head>
<body data-root="{prefix}"><a class="skip" href="#main">Skip to content</a>
<aside class="sidebar" id="course-navigation" aria-label="Course navigation"><a class="brand" href="{prefix}index.html"><span class="brand-icon">&lt;/&gt;</span><span>{esc(self.config['code'])}<small>THE PYTHON CLASSROOM</small></span></a><p class="nav-label">YOUR CLASSROOM</p><nav aria-label="Main">{menu}</nav><p class="nav-label weeks-label">WEEKLY MATERIALS</p><nav aria-label="Weeks">{weekly}</nav><div class="sidebar-bottom"><div class="sidebar-note"><strong>Small steps. Real progress.</strong>Read it. Trace it. Run it.<br>Then make it your own.</div><a href="{esc(self.config['repository'])}">{icon('branch')} View repository <span aria-hidden="true">↗</span></a></div></aside>
<div class="shell"><header class="topbar"><button class="menu-toggle" aria-label="Toggle navigation" aria-controls="course-navigation" aria-expanded="false">{icon('menu')}</button><span><strong>Course materials</strong><span class="course-name"> &nbsp; / &nbsp; {esc(self.config['name'])}</span></span><span class="term"><span class="status-dot"></span>{esc(self.config['term'])}</span></header><main class="content" id="main">{body}<footer class="footer"><span>{esc(self.config['code'])} · {esc(self.config['term'])} · {esc(self.config['instructor'])}</span><span><a href="{esc(self.config['repository'])}">Made for learning, shared on GitHub ↗</a></span></footer></main></div></body></html>'''
        path = self.out / current
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(page, encoding='utf-8')

    def breadcrumbs(self, current, label, week=None):
        middle = f'<span>/</span><a href="{self.link(f"weeks/week-{week}.html", current)}">Week {week}</a>' if week else ''
        return f'<div class="breadcrumbs"><a href="{self.link("index.html", current)}">Course overview</a>{middle}<span>/</span><span>{esc(label)}</span></div>'

    def build(self):
        self.out.mkdir(parents=True, exist_ok=True)
        shutil.copytree(self.root / 'site/assets', self.out / 'assets', dirs_exist_ok=True)
        (self.out / '.nojekyll').touch()
        for item in self.files:
            dest = self.out / 'downloads' / item['path']
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(self.root / item['path'], dest)
        self.home()
        self.resources()
        self.links()
        self.guides()
        for week in self.weeks:
            self.week(week)
        for item in self.files:
            self.viewer(item)
        print(f'Built {len(self.files)} materials across {len(self.weeks)} weeks in {self.out}')

    def home(self):
        python_count = sum(item['kind'] == 'PY' for item in self.files)
        pdf_count = sum(item['kind'] == 'PDF' for item in self.files)
        cards = []
        for week in self.weeks:
            info = self.week_info(week)
            count = sum(item['week'] == week and item['kind'] == 'PY' for item in self.files)
            tags = ''.join(f'<span class="tag">{esc(tag)}</span>' for tag in info['tags'])
            cards.append(f'<a class="week-card" href="weeks/week-{week}.html"><div class="card-top"><span class="week-number">{week:02d}</span><span class="badge">WEEK {week:02d}</span></div><h3>{esc(info["title"])}</h3><p>{esc(info["description"])}</p><div class="tags">{tags}</div><div class="card-footer"><span>{count} Python {"example" if count == 1 else "examples"} · View materials</span><span class="arrow">{icon("arrow")}</span></div></a>')
        entries = []
        for item in self.files:
            info = self.week_info(item['week']) if item['week'] else {'title': '', 'tags': []}
            search = ' '.join([item['title'], item['path'], item['text'], info['title'], *info['tags'], f'week {item["week"]}' if item['week'] else 'resources']).lower()
            entries.append({key: item[key] for key in ['title', 'path', 'kind', 'url']} | {'search': search})
        kinds = ''.join(f'<option value="{esc(kind)}">{esc(kind)}</option>' for kind in sorted({item['kind'] for item in self.files}))
        data = json.dumps(entries, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
        self.write('index.html', 'Your Python classroom', f'''<section class="hero"><div><p class="eyebrow">A LITTLE CURIOSITY. A LOT OF POSSIBILITY.</p><h1>Your next line<br>starts here<span style="color:#7d9a56">.</span></h1><p>Your home for Python examples, classroom exercises, and those “oh, now I get it” moments. Pick a week and explore.</p><div class="hero-actions"><a class="button primary" href="#weekly-materials">Explore the materials {icon('arrow')}</a><a class="button-link" href="getting-started.html">New to Python? Start here ↗</a></div></div><div class="hello-art" aria-label="Python example: print Hello, world!"><div class="art-grid"></div><div class="code-window"><div class="code-top"><i></i><i></i><i></i><span>your_first_program.py</span></div><pre><span class="dim"># Every programmer starts somewhere.</span>
<span class="yellow">message</span> = <span class="yellow">"Hello, world!"</span>
print(message)
<span class="output">&gt; Hello, world!</span></pre></div><span class="art-note">One line at a time ✦</span></div></section>
<div class="stats"><span><strong>{len(self.weeks):02d}</strong> weeks to explore</span><span><strong>{python_count:02d}</strong> Python files</span><span><strong>{pdf_count:02d}</strong> exercise handouts</span><span class="grow">A place to learn by doing.</span></div>
<section aria-labelledby="weekly-materials"><div class="section-heading"><div><h2 id="weekly-materials">Find your next lesson</h2><p>Follow along in class, or revisit at your own pace.</p></div><div class="search-controls" hidden><label class="search-box">{icon('search')}<span class="visually-hidden">Search all course materials</span><input id="material-search" type="search" placeholder="Search topics or code…" autocomplete="off" aria-controls="search-results"></label><label class="type-filter"><span class="visually-hidden">Filter by file type</span><select id="material-kind" aria-controls="search-results"><option value="">All file types</option>{kinds}</select></label><button class="button small" id="clear-search" type="button" hidden>Clear search</button></div></div><p class="search-count" id="search-count" role="status" aria-live="polite"></p><div id="search-results" class="search-results" hidden></div><div id="browse-content"><div class="week-grid">{''.join(cards)}</div><div class="section-heading"><h2>A little extra practice</h2><a class="button-link" href="resources.html">All resources {icon('arrow')}</a></div><div class="resource-grid"><a class="resource-card" href="resources.html#exercises"><span class="resource-icon">{icon('file')}</span><span><strong>In-class exercises</strong><small>Put the concepts into practice.</small></span><span class="arrow">↗</span></a><a class="resource-card" href="resources.html#worksheets"><span class="resource-icon">{icon('book')}</span><span><strong>Worksheets & tools</strong><small>Trace your thinking. Test your code.</small></span><span class="arrow">↗</span></a></div><a class="resource-card course-links-card" href="links.html"><span class="resource-icon">{icon("book")}</span><span><strong>Course links</strong><small>Websites and references shared in class.</small></span><span class="arrow" aria-hidden="true">↗</span></a><div class="callout">{icon('branch')}<div><strong>The code is yours to explore.</strong><p>See how this course is organized on GitHub, then download a copy and try it yourself.</p></div><a class="button-link" href="{esc(self.config['repository'])}">Open GitHub ↗</a></div></div></section><script type="application/json" id="search-data">{data}</script><noscript><p class="empty">Search needs JavaScript. All weekly materials and downloads remain available through the links on this page.</p></noscript>''')

    def week(self, week):
        current = f'weeks/week-{week}.html'
        info = self.week_info(week)
        items = [item for item in self.files if item['week'] == week]
        guide = next((item for item in items if item['path'] == f'week-{week}-demos/README.md'), None)
        rows = ''.join(self.row(item, current) for item in items if item is not guide)
        guide_html = f'<section class="prose" aria-label="Weekly guide">{self.markdown(guide["text"], guide["path"], current)}</section>' if guide else ''
        self.write(current, info['title'], self.breadcrumbs(current, f'Week {week}') + f'<div class="page-heading"><p class="eyebrow">WEEK {week:02d} · YOUR LEARNING PATH</p><h1>{esc(info["title"])}</h1><p>{esc(info["description"])}</p><a class="button-link" href="{esc(self.github(f"week-{week}-demos", "tree"))}">See this folder on GitHub ↗</a></div><div class="section-heading"><h2>Explore the examples</h2><span class="reading-label">Read → Predict → Run → Change</span></div><div class="list">{rows}</div>{guide_html}', f'week-{week}')

    def resources(self):
        current = 'resources.html'
        body = self.breadcrumbs(current, 'Exercises & resources') + '<div class="page-heading"><p class="eyebrow">PRACTICE MAKES PROGRESS</p><h1>Try it. Trace it. Understand it.</h1><p>Classroom exercises, reusable worksheets, and the tools that help you explore the code.</p></div>'
        groups = [('midterm', 'Midterm preparation · Weeks 2–5', lambda p: p.startswith('Midterm Preparation/')), ('exercises', 'In-class exercises', lambda p: p.startswith('in-class-exercise-')), ('worksheets', 'Worksheets & classroom tools', lambda p: p.startswith('utilities/')), ('more', 'More to explore', lambda p: not p.startswith(('Midterm Preparation/', 'in-class-exercise-', 'utilities/')))]
        for anchor, label, predicate in groups:
            items = [item for item in self.files if item['week'] is None and predicate(item['path'])]
            body += f'<section id="{anchor}"><div class="section-heading"><h2>{label}</h2></div>'
            body += '<div class="list">' + ''.join(self.row(item, current) for item in items) + '</div>' if items else '<p class="empty">Materials will appear here when they are added.</p>'
            body += '</section>'
        self.write(current, 'Exercises & resources', body, 'resources')

    def links(self):
        current = 'links.html'
        body = self.breadcrumbs(current, 'Course links') + '<div class="page-heading"><p class="eyebrow">KEEP THESE HANDY</p><h1>Course links</h1><p>Useful websites and references shared in class, together in one place.</p></div>'
        if self.course_links:
            body += '<div class="list">' + ''.join(
                f'<a class="file-row" href="{esc(item["url"])}">{link_logo(item["url"])}<div><strong>{esc(item["title"])}</strong><small>{esc(item["url"])}</small></div></a>'
                for item in self.course_links) + '</div>'
        else:
            body += '<p class="empty">No course links have been shared yet. Check back after class.</p>'
        self.write(current, 'Course links', body, 'links')

    def viewer(self, item):
        current = unquote(item['url'])
        week, source = item['week'], item['path']
        download = self.link('downloads/' + quote(source, safe='/'), current)
        body = self.breadcrumbs(current, item['title'], week) + f'<div class="page-heading"><p class="eyebrow">{esc(item["kind"])} · {"WEEK " + str(week) if week else "COURSE RESOURCE"}</p><h1>{esc(item["title"])}</h1><p>{esc(source)}</p></div><div class="toolbar"><a class="button primary" href="{download}" download>Download {esc(item["kind"])}</a><a class="button" href="{esc(self.github(source))}">View on GitHub ↗</a>'
        if item['kind'] == 'PDF':
            body += f'<a class="button" href="{download}">Open PDF ↗</a>'
        body += '</div>'
        if item['kind'] == 'PY':
            body += f'<p class="reading-label">Read the comments, predict the output, then try it on your computer.</p><div class="source"><div class="source-header"><span>{esc(Path(source).name)}</span><button data-copy type="button">Copy code</button></div><pre tabindex="0" aria-label="Python source code"><code id="source-code">{highlight_python(item["text"])}</code></pre></div><p id="copy-status" class="reading-label" role="status" aria-live="polite"></p>'
            body += f'<details class="run-help"><summary>How do I run this example?</summary><p>Download the repository ZIP from the getting started guide and extract it. Open a terminal in the extracted course folder, then use the command for your computer. This page displays code; it does not run Python.</p><h3>Windows</h3><code>py "{esc(source)}"</code><h3>macOS / Linux</h3><code>python3 "{esc(source)}"</code><p>Some programs ask you to type answers in the terminal. If a demo imports another course file, keep those files together.</p><a class="button-link" href="{self.link("getting-started.html", current)}">Full getting started guide {icon("arrow")}</a></details>'
        elif item['kind'] == 'MD':
            body += '<article class="prose">' + self.markdown(item['text'], source, current) + '</article>'
        elif item['kind'] == 'PDF':
            body += f'<p class="reading-label">If the preview is unavailable on your device, use Open PDF or Download PDF above.</p><iframe class="pdf-preview" src="{download}" title="{esc(item["title"])} PDF preview" loading="lazy"></iframe>'
        elif item['text']:
            body += f'<div class="source"><pre tabindex="0"><code>{esc(item["text"])}</code></pre></div>'
        else:
            body += '<div class="prose"><h2>Ready to explore?</h2><p>Download this material to open it with the appropriate app, or view it on GitHub.</p></div>'
        siblings = [entry for entry in self.files if entry['week'] == week and entry['kind'] == 'PY'] if item['kind'] == 'PY' else []
        if source.startswith('Midterm Preparation/'):
            siblings = [entry for entry in siblings if entry['path'].startswith('Midterm Preparation/')]
        else:
            siblings = [entry for entry in siblings if not entry['path'].startswith('Midterm Preparation/')]
        if item in siblings:
            index = siblings.index(item)
            body += '<nav class="pager" aria-label="More examples">'
            if index:
                body += f'<a href="{self.link(siblings[index-1]["url"], current)}">← {esc(siblings[index-1]["title"])}</a>'
            if index + 1 < len(siblings):
                body += f'<a href="{self.link(siblings[index+1]["url"], current)}">{esc(siblings[index+1]["title"])} →</a>'
            body += '</nav>'
        self.write(current, item['title'], body, 'midterm' if source.startswith('Midterm Preparation/') else f'week-{week}' if week else 'resources')

    def guides(self):
        repo = esc(self.config['repository'])
        start = '''<div class="page-heading"><p class="eyebrow">EVERYONE STARTS SOMEWHERE</p><h1>Your first steps with Python.</h1><p>You can read every example on this site without installing anything. When you’re ready to try the code, follow these steps.</p></div><div class="steps"><section class="step"><span>01 / GET PYTHON</span><h2>Set up your computer</h2><p>Install Python 3 from the official Python website. On Windows, follow the installer’s instructions for the Python launcher. If you’re using a college computer, check whether Python is already installed.</p><p><a href="https://www.python.org/downloads/">Download Python ↗</a></p></section><section class="step"><span>02 / GET THE EXAMPLES</span><h2>Make your own copy</h2><p>Open the course repository on GitHub. Choose the green Code button, then Download ZIP. Extract the ZIP into a folder you can find again. You don’t need a GitHub account to download.</p><p><a href="REPO">Open the course repository ↗</a></p></section><section class="step"><span>03 / TRY ONE PROGRAM</span><h2>Meet the terminal</h2><p>A terminal is a place to type commands. Open it in your extracted course folder (on Windows, right-click inside the folder and choose Open in Terminal). Run one example using the command below.</p></section></div><article class="prose"><h2>Start with a hello</h2><p>On <strong>Windows</strong>, type:</p><pre><code>py first_file.py</code></pre><p>On <strong>macOS or Linux</strong>, type:</p><pre><code>python3 first_file.py</code></pre><p>You should see a greeting. To try another program, replace <code>first_file.py</code> with its folder and filename. Each Python page on this site has the exact commands under “How do I run this example?”.</p><h2>Make learning an experiment</h2><ol><li><strong>Read</strong> the problem and the comments (lines beginning with <code>#</code>).</li><li><strong>Predict</strong> what the program will print. Try a trace table to follow the values.</li><li><strong>Run</strong> the original program and compare its output with your prediction.</li><li><strong>Change</strong> one value. Predict again. Run again.</li></ol><h2>If something doesn’t work</h2><ul><li><strong>Python isn’t recognized:</strong> finish installing Python, close the terminal, and open it again.</li><li><strong>File not found:</strong> check that the terminal is in the extracted course folder and that the filename is spelled correctly.</li><li><strong>The program seems to pause:</strong> look for a question. It may be waiting for you to type a response and press Enter.</li><li><strong>You see an error:</strong> read the last line first. Check the file and line number, then ask your instructor if you’re stuck.</li></ul><h2>A quick tour of GitHub</h2><p>A <strong>repository</strong> is a project’s files and their history. A <strong>commit</strong> records a change. A <strong>branch</strong> lets someone work on a separate version. A <strong>pull request</strong> proposes changes for review and merging.</p><p>Use “View on GitHub” beside any example to see its original file and history. Save your experiments in your downloaded copy; they won’t change the course repository.</p></article>'''.replace('REPO', repo)
        self.write('getting-started.html', 'Getting started', self.breadcrumbs('getting-started.html', 'Getting started') + start, 'start')
        upload = self.github('', 'upload')
        instructor = f'''<div class="page-heading"><p class="eyebrow">FOR THE INSTRUCTOR</p><h1>Add a file. Grow the classroom.</h1><p>The site is built from your course files. Keep teaching in Python and Markdown; the library takes care of the navigation and code previews.</p><a class="button primary" href="{esc(upload)}">Upload materials on GitHub ↗</a></div><article class="prose"><h2>Publish from GitHub</h2><ol><li>Sign into GitHub with write access to this repository.</li><li>Open the destination folder, choose <strong>Add file → Upload files</strong>, and drag in your materials. To write notes, use <strong>Add file → Create new file</strong>.</li><li>Commit to <code>{esc(self.config['branch'])}</code>, or open and merge a pull request if you prefer review.</li><li>Open the repository’s <strong>Actions</strong> tab. After <strong>Publish course site</strong> finishes successfully, refresh this site.</li></ol><h2>Where should files go?</h2><div class="table-scroll"><table><tr><th>Material</th><th>Location</th></tr><tr><td>Weekly code and notes</td><td><code>week-6-demos/01_my_new_demo.py</code></td></tr><tr><td>A guide for that week</td><td><code>week-6-demos/README.md</code></td></tr><tr><td>Exercise handouts and starter code</td><td><code>in-class-exercise-4/</code></td></tr><tr><td>Worksheets and classroom tools</td><td><code>utilities/</code></td></tr><tr><td>Other course materials</td><td><code>materials/</code> (subfolders welcome)</td></tr></table></div><p>A new <code>week-N-demos</code> folder appears automatically once it contains a supported material. Number files like <code>01_topic.py</code> to set a teaching sequence. Add a README with a <code># Week 6: Your topic</code> heading for a useful default title. You can optionally set a title, description, and topic tags in <code>site/course.json</code>.</p><h2>What can I upload?</h2><p>Python, Markdown, PDF, plain text, CSV, JSON, notebooks, Word, PowerPoint, Excel, ZIP files, and common image formats. Python gets a highlighted code view; Markdown gets a readable guide; PDFs get a preview. Other formats have download and GitHub links.</p><p>Use relative Markdown links to other course files. Basic headings, paragraphs, links, inline code, fenced code blocks, lists, and tables are supported. Raw HTML is shown as text. Keep any companion modules alongside their demos.</p><h2>Publish from your computer</h2><p>Add or edit course files in your usual editor, commit them, and push to the main branch (or merge your pull request). GitHub rebuilds and publishes the site automatically. There is no second copy of the teaching content to maintain.</p><h2>Before publishing</h2><p>This is a public course site. Publish student-facing materials only. The builder includes supported files inside course folders, including subfolders. Hidden files and build folders are excluded. Keep solutions, grades, and private notes outside those folders and outside the public repository.</p><p><a href="{repo}/actions">View publishing status ↗</a> · <a href="{esc(self.github('site/README.md'))}">Site maintenance guide ↗</a></p></article>'''
        self.write('instructor.html', 'For the instructor', self.breadcrumbs('instructor.html', 'For the instructor') + instructor, 'instructor')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / '_site')
    args = parser.parse_args()
    # Build into an empty directory so deleted materials can never survive a deployment.
    if args.output.exists() and any(args.output.iterdir()):
        parser.error('Output directory must be empty. Use a fresh output path or remove only the old generated _site directory.')
    Site(ROOT, args.output).build()


if __name__ == '__main__':
    main()
