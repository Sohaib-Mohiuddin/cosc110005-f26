"""Navigation hierarchy, exact selection, and unpublished-content boundaries."""
import shutil
import subprocess
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

from build import ROOT, Site

CONTEXT_LABELS = {'Section', 'Released weeks', 'Current week', 'Released assignments', 'Assignment materials'}


class Navigation(HTMLParser):
    def __init__(self):
        super().__init__()
        self.navs = []
        self.current = None
        self.link = None
        self.body = {}

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'body':
            self.body = attrs
        if tag == 'nav':
            self.current = {**attrs, 'links': []}
            self.navs.append(self.current)
        if tag == 'a' and self.current is not None:
            self.link = {**attrs, 'text': ''}
            self.current['links'].append(self.link)

    def handle_data(self, value):
        if self.link is not None:
            self.link['text'] += value

    def handle_endtag(self, tag):
        if tag == 'a':
            self.link = None
        if tag == 'nav':
            self.current = None


class NavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temporary.name)
        cls.site = Site(ROOT, cls.output)
        cls.site.build()

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def parse(self, route):
        parsed = Navigation()
        parsed.feed((self.output / route).read_text(encoding='utf-8'))
        return parsed

    def test_primary_navigation_has_five_sections_with_one_current_section(self):
        routes = {
            'index.html': 'Course', 'getting-started.html': 'Course',
            'resources.html': 'Course', 'links.html': 'Course',
            'concepts.html': 'Course', 'assignments.html': 'Assignments',
            'assignments/assignment-1.html': 'Assignments',
            'view/Assignment-1/brief.md.html': 'Assignments',
            'practice.html': 'Practice', 'workspace.html': 'Workspace',
            'study.html': 'My Study', 'updates.html': 'Course',
        }
        for route, section in routes.items():
            with self.subTest(route=route):
                parsed = self.parse(route)
                primary = next(nav for nav in parsed.navs if nav.get('id') == 'primary-navigation')
                self.assertEqual(primary.get('aria-label'), 'Primary')
                self.assertEqual([link['text'].strip() for link in primary['links']],
                                 ['Course', 'Assignments', 'Practice', 'Workspace', 'My Study'])
                selected = [link for link in primary['links'] if link.get('aria-current')]
                self.assertEqual([(link['text'].strip(), link['aria-current']) for link in selected],
                                 [(section, 'true')])
                if route in {'workspace.html', 'practice.html'}:
                    self.assertEqual(parsed.body.get('data-layout'), 'embedded')

    def test_context_current_page_always_resolves_to_the_page_being_viewed(self):
        for page in self.output.rglob('*.html'):
            route = page.relative_to(self.output).as_posix()
            parsed = self.parse(route)
            for nav in parsed.navs:
                if nav.get('aria-label') not in CONTEXT_LABELS:
                    continue
                for link in nav['links']:
                    if link.get('aria-current') != 'page':
                        continue
                    target = urlsplit(urljoin('https://course.example/' + route, link['href']))
                    self.assertEqual(unquote(target.path).lstrip('/'), route, (route, link))
                    self.assertFalse(target.fragment, (route, link))
        for route in ['index.html', 'weeks/week-3.html', 'assignments/assignment-1.html', 'view/Assignment-1/brief.md.html']:
            parsed = self.parse(route)
            selected = [link for nav in parsed.navs
                        if nav.get('aria-label') in CONTEXT_LABELS
                        for link in nav['links'] if link.get('aria-current') == 'page']
            self.assertEqual(len(selected), 1, route)

    def test_untracked_future_weeks_and_assignments_never_enter_navigation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'site').mkdir()
            shutil.copyfile(ROOT / 'site/course.json', root / 'site/course.json')
            shutil.copytree(ROOT / 'site/assets', root / 'site/assets', ignore=shutil.ignore_patterns('__pycache__'))
            for name in ['week-3-demos/public.py', 'week-8-demos/private.py',
                         'Assignment-1/brief.md', 'Assignment-2/private.md', 'Assignment-3/private.md']:
                path = root / name
                path.parent.mkdir(exist_ok=True)
                path.write_text('# Course material\n', encoding='utf-8')
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            subprocess.run(['git', '-C', str(root), 'add', 'week-3-demos', 'Assignment-1'], check=True)
            site = Site(root, root / 'output')
            site.build()
            for page in site.out.rglob('*.html'):
                parsed = Navigation(); parsed.feed(page.read_text(encoding='utf-8'))
                links = '\n'.join(link['href'] + ' ' + link['text'] for nav in parsed.navs for link in nav['links'])
                for private in ['week-8', 'Week 08', 'Assignment-2', 'Assignment 2', 'Assignment-3', 'Assignment 3']:
                    self.assertNotIn(private, links, page)
            parsed = Navigation(); parsed.feed((site.out / 'index.html').read_text(encoding='utf-8'))
            weeks = next(nav for nav in parsed.navs if nav.get('aria-label') == 'Released weeks')
            self.assertEqual(len(weeks['links']), 1)


if __name__ == '__main__':
    unittest.main()
