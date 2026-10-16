"""Primary sections and contextual links, built only from released course files."""
import html
import re
from urllib.parse import quote, unquote, urlsplit, urlunsplit


def esc(value):
    return html.escape(str(value), quote=True)


def navigation(site, current, active, icon):
    section = {'assignments': 'assignments', 'practice': 'practice', 'workspace': 'workspace',
               'study': 'study'}.get(active, 'course')
    labels = {'course': 'Course', 'assignments': 'Assignments', 'practice': 'Practice',
              'workspace': 'Workspace', 'study': 'My Study'}
    layout = 'embedded' if section in {'workspace', 'practice'} else 'sidebar'
    material = next((item for item in site.files if unquote(item['url']) == current), None)

    def href(target):
        parts = urlsplit(target)
        path = site.link(parts.path, current) if parts.path else ''
        return esc(urlunsplit(('', '', path, parts.query, quote(parts.fragment, safe='-'))))

    def link(target, label, symbol='', branch=False):
        parts = urlsplit(target)
        selected = unquote(parts.path) == current and not parts.query and not parts.fragment
        classes = 'nav-link' + (' active' if selected else '') + (' current-branch' if branch and not selected else '')
        return (f'<a class="{classes}" href="{href(target)}"'
                + (' aria-current="page"' if selected else '')
                + f'>{symbol}<span>{esc(label)}</span></a>')

    def group(label, links):
        return f'<p class="nav-label">{esc(label)}</p><nav aria-label="{esc(label)}">{"".join(links)}</nav>'

    sections = [('index.html', 'Course', 'course'), ('assignments.html', 'Assignments', 'assignments'),
                ('practice.html', 'Practice', 'practice'), ('workspace.html', 'Workspace', 'workspace'),
                ('study.html', 'My Study', 'study')]
    primary = ''.join(f'<a class="primary-link" href="{href(target)}"'
                      + (' aria-current="true"' if section == key else '')
                      + f'>{label}</a>' for target, label, key in sections)

    context = ''
    if section == 'course':
        context = group('Section', [
            link('index.html', 'Course overview', icon('grid')),
            link('getting-started.html', 'Getting started', icon('code')),
            link('concepts.html', 'Learn by concept', icon('book')),
            link('resources.html', 'Exercises & resources', icon('file'), branch=active == 'resources'),
            link('links.html', 'Course links', icon('book')),
            *([link(site.by_path['Midterm Preparation/README.md']['url'], 'Midterm preparation', icon('book'), branch=active == 'midterm')]
              if 'Midterm Preparation/README.md' in site.by_path else []),
            link('updates.html', 'What’s new', icon('branch')),
        ])
        week = material['week'] if material else None
        match = re.fullmatch(r'weeks/week-(\d+)\.html', current)
        if match:
            week = int(match[1])
        context += group('Released weeks', [link(f'weeks/week-{number}.html', f'Week {number:02d}',
                          f'<span class="week-dot">{number:02d}</span>', branch=week == number)
                          for number in site.weeks])
        if week in site.weeks:
            context += group('Current week', [link(item['url'], item['title']) for item in site.files if item['week'] == week])
        elif material:
            folder = material['path'].split('/')[0]
            context += group('Current materials', [link(item['url'], item['title']) for item in site.files
                             if item['assignment'] is None and item['week'] is None and item['path'].split('/')[0] == folder])
        elif active == 'concepts' and site.studio.topics:
            context += group('Concepts', [link('concepts.html#' + topic['id'], topic['title']) for topic in site.studio.topics])
    elif section == 'assignments':
        number = material['assignment'] if material else None
        match = re.fullmatch(r'assignments/assignment-(\d+)\.html', current)
        if match:
            number = int(match[1])
        context = group('Section', [link('assignments.html', 'All assignments', icon('file'))])
        context += group('Released assignments', [link(f'assignments/assignment-{released}.html', f'Assignment {released}', branch=number == released)
                                                  for released in site.assignment_numbers])
        if number in site.assignment_numbers:
            info = site.assignment_info(number)
            context += group('Assignment materials', [link(item['url'], 'Readable brief' if item is info.get('reading')
                                else 'Original PDF' if item is info['brief'] and item['kind'] == 'PDF' else item['title'])
                                for item in info['items']])
        if not site.assignment_numbers:
            context += '<p class="context-empty">Assignments appear here when they are released.</p>'
    elif section == 'practice':
        context = group('Section', [link('practice.html', 'All practice', icon('code'))])
        context += group('Practice topics', [link('practice.html?topic=' + quote(topic['id'], safe='') + '#practice-activities', topic['title'])
                                            for topic in site.studio.topics])
    elif section == 'workspace':
        context = group('Section', [link('workspace.html', 'Python workspace', icon('code'))])
        context += '<p class="context-empty">Choose a project and use the Files panel to switch between its files.</p>'
    elif section == 'study':
        context = group('Section', [
            link('study.html', 'My study overview', icon('grid')),
            link('study.html#study-materials', 'Saved materials', icon('book')),
            link('study.html?show=queue#study-materials', 'Study queue'),
            link('study.html?show=bookmarked#study-materials', 'Bookmarks'),
            link('study.html?show=notes#study-materials', 'Notes'),
            link('study.html#study-backup', 'Backups', icon('file')),
            link('study.html#offline-packs', 'Offline downloads', icon('book')),
        ])

    header = f'''<header class="topbar navigation-header">
<a class="brand" href="{href('index.html')}" aria-label="{esc(site.config['code'])} course overview"><span class="brand-icon" aria-hidden="true">&lt;/&gt;</span><span class="brand-name">{esc(site.config['code'])}<small class="brand-tagline">THE PYTHON CLASSROOM</small></span></a>
<button class="menu-toggle" type="button" aria-label="Toggle navigation" aria-controls="course-navigation" aria-expanded="false">{icon('menu')}<span>Menu</span></button>
<button class="section-toggle button small" id="section-toggle" type="button" aria-label="Hide section navigation" aria-controls="course-navigation" aria-expanded="true">{icon('menu')}</button>
<nav id="primary-navigation" class="primary-navigation" aria-label="Primary">{primary}</nav>
<div class="topbar-tools"><a class="button small search-shortcut" href="{href('index.html#weekly-materials')}" aria-label="Search materials">{icon('search')}<span>Search</span></a><button class="button small" id="open-reference" type="button">Reference</button><button class="button small" id="open-display" type="button">Display</button></div>
</header>'''
    sidebar = f'''<aside class="sidebar" id="course-navigation" aria-label="{esc(labels[section])} navigation">
<div class="context-heading"><strong>{esc(labels[section])}</strong><button class="drawer-close button small" id="close-navigation" type="button" aria-label="Close navigation">Close</button></div>
<nav class="mobile-primary-navigation" aria-label="Primary sections">{primary}</nav>
{context}<div class="sidebar-bottom"><a href="{esc(site.config['repository'])}">{icon('branch')} View repository <span aria-hidden="true">↗</span></a></div></aside>'''
    return {'header': header, 'sidebar': sidebar, 'section': section, 'layout': layout}
