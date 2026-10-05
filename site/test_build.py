"""Regression checks for discovery, safe previews, and deployable project-relative links."""
import json
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from build import ROOT, Site, discover, highlight_python


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for attribute in ('href', 'src'):
            if attribute in attrs:
                self.links.append(attrs[attribute])

    def handle_data(self, data):
        self.text.append(data)


class CourseSiteTests(unittest.TestCase):
    def test_new_week_nested_files_and_exclusions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ['week-6-demos/01_new.py', 'week-6-demos/examples/a & b.py', 'week-6-demos/.private/notes.md', 'week-6-demos/__pycache__/cached.py', 'materials/lecture 1.pdf', '.env', 'site/private.py', 'in-class-exercise-4/task.txt']:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('print("hi")', encoding='utf-8')
            files = discover(root)
            self.assertEqual(len(files), 4)
            self.assertEqual({file['week'] for file in files}, {6, None})
            self.assertTrue(any('a%20%26%20b.py' in file['url'] for file in files))

    def test_highlight_preserves_source_and_escapes_html(self):
        source = '# <script>alert("hi")</script>\ntext = "<hello>"\nprint(text)\n'
        markup = highlight_python(source)
        self.assertNotIn('<script>', markup)
        parser = Links(); parser.feed(markup)
        self.assertEqual(''.join(parser.text), source)
        self.assertIn('tok-comment', markup)
        self.assertIn('tok-string', markup)

    def test_incomplete_python_still_displays(self):
        source = 'if True:\n    print("hello"\n'
        parser = Links(); parser.feed(highlight_python(source))
        self.assertEqual(''.join(parser.text), source)

    def test_all_generated_local_links_resolve(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            site = Site(ROOT, output)
            site.build()
            self.assertEqual(len(list((output / 'view').rglob('*.html'))), len(site.files))
            for page in output.rglob('*.html'):
                parser = Links(); parser.feed(page.read_text(encoding='utf-8'))
                for link in parser.links:
                    parts = urlsplit(link)
                    if parts.scheme or parts.netloc:
                        continue
                    self.assertFalse(link.startswith('/'), f'Root-relative link breaks project Pages: {link}')
                    target = (page.parent / unquote(parts.path)).resolve() if parts.path else page
                    self.assertTrue(target.is_relative_to(output.resolve()))
                    self.assertTrue(target.exists(), f'{page}: missing {link}')
                    if parts.fragment and target.suffix == '.html':
                        target_parser = Links(); target_parser.feed(target.read_text(encoding='utf-8'))
                        self.assertIn(parts.fragment, target_parser.ids, f'{page}: missing anchor {link}')
            for item in site.files:
                self.assertEqual((ROOT / item['path']).read_bytes(), (output / 'downloads' / item['path']).read_bytes())

    def test_future_week_and_safe_markdown(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'site').mkdir()
            (root / 'site/course.json').write_text((ROOT / 'site/course.json').read_text(encoding='utf-8'), encoding='utf-8')
            folder = root / 'week-15-demos'; folder.mkdir()
            (folder / 'README.md').write_text('# Week 15: A new topic\n', encoding='utf-8')
            (folder / '01_a & b.py').write_text('print("yes")', encoding='utf-8')
            site = Site(root, root / '_site')
            self.assertEqual(site.weeks, [15])
            self.assertEqual(site.week_info(15)['title'], 'A new topic')
            rendered = site.markdown('[Demo](01_a%20%26%20b.py)\n\n<script>bad()</script>\n\n[Bad](javascript:alert)\n', 'week-15-demos/README.md', 'view/week-15-demos/README.md.html')
            self.assertIn('01_a%20%26%20b.py.html', rendered)
            self.assertNotIn('<script>', rendered)
            self.assertNotIn('href="javascript:', rendered)


if __name__ == '__main__':
    unittest.main()
