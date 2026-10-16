"""Learning features generated exclusively from the site's released material list."""
import ast
import html
import json
import posixpath
import zipfile
from pathlib import Path
from urllib.parse import quote, unquote


def json_script(value):
    return json.dumps(value, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')


class Learning:
    def __init__(self, site):
        self.site = site
        self.cases = {}
        for path in ['utilities/demo_cases.json', 'site/practice_cases.json']:
            source = site.root / path
            if source.exists():
                self.cases.update(json.loads(source.read_text(encoding='utf-8')))
        value_checks = site.root / 'site/value_checks.json'
        if value_checks.exists():
            for path, assertions in json.loads(value_checks.read_text()).items():
                for case in self.cases.get(path, {}).get('cases', []):
                    case['assertions'] = assertions
        self.groups = {}
        for item in site.files:
            key = item['path'].split('/')[0] if '/' in item['path'] else 'first-examples'
            self.groups.setdefault(key, []).append(item)
        self._companions = {}

    def group(self, item):
        return item['path'].split('/')[0] if '/' in item['path'] else 'first-examples'

    def companions(self, item):
        """Include folder contents and uniquely identifiable imported course modules."""
        key = self.group(item)
        if key in self._companions:
            return self._companions[key]
        selected = {entry['path']: entry for entry in self.groups[key]}
        pending = list(selected.values())
        while pending:
            entry = pending.pop()
            if entry['kind'] != 'PY':
                continue
            try:
                tree = ast.parse(entry['text'])
            except SyntaxError:
                continue
            modules = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    modules.extend(alias.name.split('.')[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    modules.append(node.module.split('.')[0])
            for module in modules:
                local = posixpath.join(posixpath.dirname(entry['path']), module + '.py')
                matches = [candidate for candidate in self.site.files if candidate['kind'] == 'PY' and Path(candidate['path']).stem == module]
                dependency = self.site.by_path.get(local) or (matches[0] if len(matches) == 1 else None)
                if dependency and dependency['path'] not in selected:
                    selected[dependency['path']] = dependency
                    pending.append(dependency)
        self._companions[key] = list(selected.values())
        return self._companions[key]

    def desktop_reason(self, item):
        unsupported = {'tkinter', 'turtle', 'subprocess', 'multiprocessing', 'socket', 'ctypes'}
        # Only the selected program and its actual imports determine compatibility.
        pending, seen = [item], set()
        companions = self.companions(item)
        while pending:
            entry = pending.pop()
            if entry['path'] in seen:
                continue
            seen.add(entry['path'])
            try:
                nodes = ast.walk(ast.parse(entry['text']))
            except SyntaxError:
                continue  # Let students repair incomplete code in the editor.
            for node in nodes:
                modules = [alias.name.split('.')[0] for alias in node.names] if isinstance(node, ast.Import) else [node.module.split('.')[0]] if isinstance(node, ast.ImportFrom) and node.module else []
                for module in modules:
                    if module in unsupported:
                        return f'This example uses {module}, which needs desktop Python.'
                    pending.extend(other for other in companions if other['kind'] == 'PY' and Path(other['path']).stem == module)
        return ''

    def bundle_url(self, item):
        return 'bundles/' + quote(self.group(item), safe='') + '.zip'

    def build_bundles(self):
        folder = self.site.out / 'bundles'
        folder.mkdir(exist_ok=True)
        for key, items in self.groups.items():
            entries = {entry['path']: entry for entry in self.companions(items[0])}
            with zipfile.ZipFile(folder / (key + '.zip'), 'w', zipfile.ZIP_DEFLATED) as archive:
                for path in sorted(entries):
                    archive.write(self.site.root / path, path)
                if items[0].get('assignment') is not None:
                    archive.writestr('READ_ASSIGNMENT.txt', 'Extract this ZIP and keep the folders together.\nRead the assignment brief for the full requirements, due date, and submission instructions.\nThe included files are course materials. Complete and submit your own work as instructed in the brief.\n')
                else:
                    archive.writestr('RUN_LESSON.txt', 'Extract this whole ZIP. Keep the folders together.\nOpen a terminal in the extracted folder and run:\npython3 "folder/example.py"\nOn Windows use py instead of python3. Replace folder/example.py with the desired file.\nGUI examples require desktop Python with Tkinter.\n')

    def controls(self, item):
        esc = html.escape
        reason = self.desktop_reason(item)
        body = '''<div class="reading-controls" hidden><label>Code size <select aria-label="Code size" id="code-size"><option value="14">Standard</option><option value="16">Large</option><option value="18">Extra large</option></select></label><label><input id="code-wrap" type="checkbox"> Wrap long lines</label></div>'''
        body += f'<div class="practice-progress" data-path="{esc(item["path"], quote=True)}" data-title="{esc(item["title"], quote=True)}" hidden><label><input id="lesson-complete" type="checkbox"> I have practised this example</label><span id="progress-save" role="status"></span></div>'
        if reason:
            return body + f'<p class="compatibility"><strong>Requires desktop Python.</strong> {esc(reason)} Download the lesson ZIP to keep companion files together.</p>'
        cases = self.cases.get(item['path'], {}).get('cases', [])
        payload = {'path': item['path'], 'cases': cases,
                   'files': [{'path': entry['path'], 'url': self.site.link('downloads/' + quote(entry['path'], safe='/'), unquote(item['url']))} for entry in self.companions(item) if entry['kind'] in {'PY', 'TXT', 'CSV', 'JSON'}]}
        body += f'<p><a class="button" href="{self.site.link("workspace.html", unquote(item["url"]))}?lesson={quote(item["path"], safe="")}">Open as my workspace project →</a></p>'
        body += '''<details class="runner" id="python-runner" hidden><summary>Try Python in your browser</summary>
<p>Edit your own copy, predict the output, then run it. Python loads on your first run. Your code runs on this device.</p>
<label for="python-editor">Your Python code</label><textarea id="python-editor" spellcheck="false" autocapitalize="off" autocomplete="off" wrap="off" aria-describedby="editor-help"></textarea>
<p id="editor-help" class="reading-label">Tab moves to the next control. Use spaces to indent. Ctrl+Enter or Command+Enter runs your code.</p>
<label for="python-input">Program input</label><textarea id="python-input" rows="3" spellcheck="false" aria-describedby="input-help" placeholder="One answer per line"></textarea>
<p id="input-help" class="reading-label">Enter answers before running, one per line, including any stop value such as 0 or quit. A blank line supplies an empty answer. Each run starts fresh.</p>
<div class="runner-actions"><button class="button primary" id="run-python" type="button">Run</button><button class="button" id="trace-python" type="button">Trace code</button><button class="button" id="stop-python" type="button" disabled>Stop</button><button class="button" id="reset-python" type="button">Reset code</button><button class="button" id="download-python" type="button">Download my code</button></div>
<p id="save-status" class="reading-label" role="status"></p><p id="runner-status" role="status" aria-live="polite">Ready when you are.</p>
<section id="runner-error" class="error-coach" hidden></section><h3 id="output-heading">Output</h3><pre id="python-output" tabindex="0" aria-labelledby="output-heading"></pre><section id="runner-trace" class="trace-view" hidden></section>'''
        if cases:
            body += '<section class="practice-checks"><h3>Check my work</h3><p>These sample checks give practice feedback, not a grade. They check output fragments; they do not prove your algorithm, comments, or every possible input is correct. Review the requirements and add your own cases.</p><p>For exercises with supplied variables, each check temporarily substitutes the values shown below. Your saved code stays unchanged.</p><button class="button" id="check-python" type="button">Run sample checks</button><ol id="check-results" aria-live="polite"></ol><details><summary>View sample inputs and expected output</summary><div class="sample-cases">'
            for index, case in enumerate(cases, 1):
                body += f'<h4>Case {index}: {esc(case.get("label", "Sample output"))}</h4>'
                if case.get('overrides'):
                    body += '<p>Supplied variables</p><pre>' + esc(json.dumps(case['overrides'], indent=2)) + '</pre>'
                if case.get('assertions'):
                    body += '<p>Named value checks</p><pre>' + esc(json.dumps(case['assertions'], indent=2)) + '</pre>'
                body += '<p>Program input</p><pre>' + esc(case.get('stdin') or '(none)') + '</pre><p>Expected output includes</p><pre>' + esc('\n'.join(case['contains'])) + '</pre>'
            body += '</div></details></section>'
        body += '<details class="custom-tests"><summary>Try your own expected result</summary><label>Expected output<textarea id="lesson-expected" rows="3"></textarea></label><label>Compare as<select id="lesson-mode"><option value="exact">Exact text</option><option value="number">One number</option><option value="json">JSON values</option><option value="contains">Contains text</option></select></label><label>Numeric tolerance<input id="lesson-tolerance" type="number" min="0" step="any" value="0"></label><button id="lesson-test" class="button" type="button">Check my expected result</button><div id="lesson-test-result" role="status"></div></details>'
        body += '</details><script type="application/json" id="runner-data">' + json_script(payload) + '</script>'
        body += f'<script src="{self.site.link("assets/runner.js", unquote(item["url"]))}" defer></script>'
        return body
