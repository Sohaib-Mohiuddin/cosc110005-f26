"""Generate the student studio from released materials and authored practice data."""
import fnmatch
import hashlib
import html
import json
import subprocess
from pathlib import Path
from urllib.parse import quote

from learning import json_script


def esc(value):
    return html.escape(str(value), quote=True)


class Studio:
    def __init__(self, site):
        self.site = site
        self.topics = self.read('concepts.json', [])
        self.activities = self.read('activities.json', [])
        maximum = max(site.weeks, default=0)
        self.topics = [topic for topic in self.topics if topic.get('week', 0) <= maximum]
        ids = {topic['id'] for topic in self.topics}
        self.activities = [activity for activity in self.activities if activity['topic'] in ids]

    def read(self, name, default):
        path = self.site.root / 'site' / name
        return json.loads(path.read_text()) if path.exists() else default

    def page(self, path, title, body, active, script=None):
        if script:
            body += f'<script src="assets/{script}" defer></script>'
        self.site.write(path, title, body, active)

    def heading(self, eyebrow, title, description):
        return f'<div class="page-heading studio-heading"><p class="eyebrow">{esc(eyebrow)}</p><h1>{esc(title)}</h1><p>{esc(description)}</p></div>'

    def build(self):
        self.data()
        self.workspace()
        self.practice()
        self.concepts()
        self.study()
        self.news()
        self.site.write('offline.html', 'Offline', self.heading('YOUR SAVED CLASSROOM', 'You’re offline.', 'Open your saved study tools or reconnect to load a lesson that has not been downloaded.') + '<div class="runner-actions"><a class="button primary" href="workspace.html">Open workspace</a><a class="button" href="study.html#offline-packs">Saved lesson packs</a><a class="button" href="index.html">Course overview</a></div>', 'study')
        self.offline()

    def data(self):
        items = []
        for item in self.site.files:
            entry = {key: item[key] for key in ['path', 'title', 'kind', 'url', 'week', 'assignment']}
            entry['url'] = item['url']
            if item['kind'] == 'PY':
                entry['files'] = [{'path': companion['path'], 'url': 'downloads/' + quote(companion['path'], safe='/')} for companion in self.site.learning.companions(item) if companion['kind'] in {'PY', 'TXT', 'CSV', 'JSON'}]
                entry['desktop'] = self.site.learning.desktop_reason(item)
            items.append(entry)
        topics = []
        for topic in self.topics:
            topic = dict(topic)
            topic['materials'] = [item['path'] for item in self.site.files if any(fnmatch.fnmatch(item['path'], pattern) for pattern in topic.get('patterns', []))]
            topic['prerequisites'] = [key for key in topic.get('prerequisites', []) if any(other['id'] == key for other in self.topics)]
            topics.append(topic)
        data = {'materials': items, 'topics': topics, 'activities': self.activities, 'reference': self.read('reference.json', [])}
        (self.site.out / 'study-data.json').write_text(json_script(data), encoding='utf-8')

    def workspace(self):
        body = self.heading('YOUR IDEAS. YOUR CODE.', 'Python workspace', 'Create a project, experiment with a lesson, and keep your work. Projects save in this browser; export important work to use it elsewhere.')
        body += '''<div id="workspace-app" class="workspace-app" hidden>
<div class="project-toolbar"><label>Project <select id="project-select" aria-label="Choose project"></select></label><label>Project name <input id="project-name" maxlength="80" value="My first project"></label><button class="button" id="new-project">New project</button><button class="button" id="snapshot-project">Save a copy</button><button class="button" id="export-project">Export project ZIP</button><button class="button" id="delete-project">Remove project</button></div>
<p id="workspace-save" role="status"></p><div class="workspace-layout"><aside class="project-files" aria-label="Project files"><div class="section-heading"><h2>Files</h2><label class="button small upload-label">Open files<input id="import-files" type="file" multiple accept=".py,.txt,.csv,.json,.md"></label></div><div id="file-list" class="file-list"></div><label>New file name<input id="new-file-name" placeholder="helper.py" maxlength="180"></label><button class="button small" id="add-file">Add file</button><details><summary>Rename or remove</summary><label>File name<input id="rename-file-name" maxlength="180"></label><div class="runner-actions"><button class="button small" id="rename-file">Rename</button><button class="button small" id="delete-file">Remove file</button></div></details></aside>
<section class="workspace-code" aria-label="Code and execution"><div class="editor-toolbar"><label for="workspace-editor" id="active-file-label">main.py</label><div class="runner-actions"><button class="button small" id="indent-code">Indent</button><button class="button small" id="unindent-code">Unindent</button><button class="button small" id="syntax-check">Check syntax</button></div></div><textarea id="workspace-editor" spellcheck="false" autocapitalize="off" wrap="off" aria-describedby="workspace-keyboard"></textarea><p id="workspace-keyboard" class="reading-label">Enter keeps indentation. Ctrl+[ / Ctrl+] adjust indentation. Tab moves to the next control. Ctrl+Enter or Command+Enter runs the entry point.</p>
<div class="execution-settings"><label>Run file<select id="entry-file"></select></label><label>Program input<textarea id="workspace-input" rows="3" placeholder="One answer per line"></textarea></label></div><div class="runner-actions"><button class="button primary" id="workspace-run">Run project</button><button class="button" id="workspace-trace">Trace project</button><button class="button" id="workspace-stop" disabled>Stop</button></div><p id="workspace-status" role="status" aria-live="polite">Ready to explore.</p><section id="workspace-error" class="error-coach" hidden></section><h2 id="workspace-output-heading">Output</h2><pre id="workspace-output" class="console-output" tabindex="0" aria-labelledby="workspace-output-heading"></pre><div id="generated-files"></div><section id="workspace-trace-view" class="trace-view" hidden></section>
<details class="custom-tests"><summary>Build your own test</summary><p>Compare the output of a fresh run, or check values and function calls. These checks are for your practice.</p><label>Expected output<textarea id="test-expected" rows="3"></textarea></label><label>Compare as<select id="test-mode"><option value="exact">Exact text</option><option value="number">One number</option><option value="json">JSON values</option><option value="contains">Contains text</option></select></label><label>Numeric tolerance<input id="test-tolerance" type="number" min="0" step="any" value="0"></label><label>Optional expression<input id="test-expression" placeholder="total or calculate(3)"></label><label>Expected expression value (JSON)<input id="test-value" placeholder="12"></label><button class="button" id="workspace-test">Run my test</button><div id="workspace-test-result" role="status"></div></details></section></div></div>
<noscript><p class="empty">The workspace needs JavaScript. Course examples and downloads remain available from the course overview.</p></noscript>'''.replace('\n+', '\n')
        self.page('workspace.html', 'Python workspace', body, 'workspace', 'workspace.js')

    def practice(self):
        body = self.heading('SMALL CHALLENGES. STRONGER THINKING.', 'Practice lab', 'Predict, complete, arrange, and debug. Try an answer first, then use hints and explanations to strengthen your understanding.')
        body += '<div class="practice-filters"><label>Concept<select id="activity-topic"><option value="">All concepts</option>' + ''.join(f'<option value="{esc(topic["id"])}">{esc(topic["title"])}</option>' for topic in self.topics) + '</select></label><label>Difficulty<select id="activity-level"><option value="">All levels</option><option value="Foundation">Foundation</option><option value="Practice">Practice</option><option value="Challenge">Challenge</option></select></label></div><p id="activity-count" role="status"></p><div class="practice-layout"><nav id="activity-list" class="activity-list" aria-label="Practice activities"></nav><section id="activity-detail" class="activity-detail" aria-live="polite"></section></div><noscript><p class="empty">Interactive activities need JavaScript. Try the downloadable practice exercises from Resources.</p></noscript>'
        self.page('practice.html', 'Practice lab', body, 'practice', 'practice.js')

    def concepts(self):
        body = self.heading('FIND THE IDEA BEHIND THE CODE.', 'Learn by concept', 'Follow the foundations in order, or revisit a topic. Each concept connects its prerequisites, released examples, and practice activities.')
        body += '<div class="concept-map">'
        for topic in self.topics:
            body += f'<a class="concept-pill" href="#{esc(topic["id"])}">{esc(topic["title"])}</a>'
        body += '</div>'
        for topic in self.topics:
            materials = [item for item in self.site.files if any(fnmatch.fnmatch(item['path'], pattern) for pattern in topic.get('patterns', []))]
            prerequisites = [other for other in self.topics if other['id'] in topic.get('prerequisites', [])]
            body += f'<section class="concept-card" id="{esc(topic["id"])}"><p class="eyebrow">{esc(topic.get("level", "Foundation"))}</p><h2>{esc(topic["title"])}</h2><p>{esc(topic["description"])}</p>'
            if prerequisites:
                body += '<p class="reading-label">Build on: ' + ', '.join(f'<a href="#{esc(other["id"])}">{esc(other["title"])}</a>' for other in prerequisites) + '</p>'
            body += '<div class="list">' + ''.join(self.site.row(item, 'concepts.html') for item in materials[:5]) + '</div>' if materials else '<p>More examples will appear as lessons are released.</p>'
            body += f'<div class="runner-actions"><a class="button primary" href="practice.html?topic={quote(topic["id"])}">Practise {esc(topic["title"].lower())}</a><a class="button" href="workspace.html">Try in workspace</a></div></section>'
        self.page('concepts.html', 'Learn by concept', body, 'concepts')

    def study(self):
        body = self.heading('MAKE ROOM FOR YOUR NEXT STEP.', 'My study space', 'Keep a study queue, revisit your notes, and move your saved work between browsers. Your progress is self-reported and stays on this device until you export it.')
        body += '''<section class="study-backup panel"><h2>Keep a portable copy</h2><p>A study backup includes projects, saved lesson edits, notes, bookmarks, progress, and preferences from this course.</p><div class="runner-actions"><button class="button primary" id="export-study">Export study backup</button><label class="button upload-label">Choose backup to restore<input type="file" id="import-study" accept=".json"></label></div><div id="backup-preview"></div><p id="backup-status" role="status"></p></section><section class="panel"><div class="section-heading"><h2>Study queue & bookmarks</h2><label>Show<select id="study-filter"><option value="all">All saved materials</option><option value="queue">Study queue</option><option value="bookmarked">Bookmarks</option><option value="Revisit">Revisit</option><option value="Practising">Practising</option><option value="Comfortable">Comfortable</option></select></label></div><div id="study-items"></div></section><section id="offline-packs" class="panel"><h2>Take lessons offline</h2><p>Save a selected pack for reading without a connection. Prepare Python separately to run standard-library console programs offline. New course releases require downloading the packs again.</p><p id="offline-status" role="status">Checking offline support…</p><div id="offline-options"></div><div class="runner-actions"><button class="button" id="prepare-python">Prepare Python for offline use</button><button class="button" id="remove-offline">Remove saved lesson packs</button></div><p id="offline-runtime" role="status"></p></section>'''
        self.page('study.html', 'My study space', body, 'study', 'study.js')

    def news(self):
        body = self.heading('YOUR CLASSROOM, GROWING.', 'What’s new', 'New learning tools, released lessons, and updated course materials.')
        body += '<section class="news-card"><span class="tag">Student studio</span><h2>A place to build your own understanding</h2><p>Create multi-file Python projects, replay code traces, try guided activities, and keep portable study backups.</p><div class="runner-actions"><a class="button primary" href="workspace.html">Open workspace</a><a class="button" href="practice.html">Try the practice lab</a></div></section>'
        changes = []
        if (self.site.root / '.git').exists():
            result = subprocess.run(['git', '-C', str(self.site.root), 'log', '-30', '--format=DATE:%aI', '--name-only', '--', *[item['path'] for item in self.site.files]], capture_output=True, text=True)
            date = ''
            seen = set()
            for line in result.stdout.splitlines():
                if line.startswith('DATE:'):
                    date = line[5:15]
                elif line in self.site.by_path and line not in seen:
                    changes.append((date, self.site.by_path[line])); seen.add(line)
        for date, item in changes[:15]:
            body += f'<article class="news-row"><time datetime="{esc(date)}">{esc(date)}</time><div><span class="reading-label">Course material updated</span><a href="{item["url"]}">{esc(item["title"])}</a><small>{esc(item["path"])}</small></div></article>'
        self.page('updates.html', 'What’s new', body, 'updates')

    def offline(self):
        root = self.site.out
        assets = ['assets/' + path.relative_to(root / 'assets').as_posix() for path in (root / 'assets').rglob('*') if path.is_file()]
        shell = ['index.html', 'workspace.html', 'practice.html', 'concepts.html', 'study.html', 'updates.html', 'offline.html', 'assignments.html', 'study-data.json', 'offline-manifest.json', 'site.webmanifest', *assets]
        packs = []
        for week in self.site.weeks:
            items = [item for item in self.site.files if item['week'] == week]
            companions = {entry['path']: entry for item in items for entry in self.site.learning.companions(item)}
            packs.append({'id': f'week-{week}', 'title': f'Week {week}: {self.site.week_info(week)["title"]}', 'urls': [self.site.learning.bundle_url(items[0]), f'weeks/week-{week}.html', *[item['url'] for item in items], *['downloads/' + quote(path, safe='/') for path in companions]]})
        for number in self.site.assignment_numbers:
            info = self.site.assignment_info(number)
            packs.append({'id': f'assignment-{number}', 'title': self.site.assignment_label(number), 'urls': [self.site.learning.bundle_url(info['items'][0]), f'assignments/assignment-{number}.html', *[item['url'] for item in info['items']], *['downloads/' + quote(item['path'], safe='/') for item in info['items']]]})
        digest = hashlib.sha256()
        for path in sorted(root.rglob('*')):
            if path.is_file() and path.name not in {'service-worker.js', 'offline-manifest.json'}:
                digest.update(path.relative_to(root).as_posix().encode()); digest.update(path.read_bytes())
        version = digest.hexdigest()[:16]
        manifest = {'version': version, 'shell': shell, 'packs': packs}
        (root / 'offline-manifest.json').write_text(json_script(manifest))
        template = (self.site.root / 'site/assets/service-worker-template.js').read_text()
        (root / 'service-worker.js').write_text(template.replace('__COURSE_VERSION__', version).replace('__COURSE_SHELL__', json.dumps(shell)))
        (root / 'site.webmanifest').write_text(json.dumps({'name': self.site.config['code'] + ' Study Studio', 'short_name': 'Python Studio', 'start_url': './index.html', 'scope': './', 'display': 'standalone', 'background_color': '#f5f7f4', 'theme_color': '#183f35', 'icons': [{'src': 'assets/favicon.svg', 'sizes': 'any', 'type': 'image/svg+xml', 'purpose': 'any'}]}))
