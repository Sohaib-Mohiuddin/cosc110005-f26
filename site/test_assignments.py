"""Assignment discovery, release boundaries, and student navigation."""
import json
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

from build import ROOT, Site, discover


class AssignmentTests(unittest.TestCase):
    def fixture(self, root, files):
        (root / 'site').mkdir()
        shutil.copytree(ROOT / 'site/assets', root / 'site/assets')
        config = json.loads((ROOT / 'site/course.json').read_text())
        config['assignments']['2'] = {'title': 'Unreleased title must stay private'}
        (root / 'site/course.json').write_text(json.dumps(config))
        for path, content in files.items():
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
        return Site(root, root / 'output')

    def test_numbered_folders_nested_files_and_numeric_order(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root, {
                'Assignment-10/brief.pdf': '%PDF-10',
                'Assignment-3/data/a & b.csv': 'score\n42',
                'assignment-2/brief.pdf': '%PDF-2',
                'Assignment-draft/private.pdf': 'private',
                'Assignment-3/.notes/private.txt': 'private',
            })
            files = discover(root)
            self.assertEqual({item['assignment'] for item in files}, {2, 3, 10})
            site = Site(root, root / 'preview')
            self.assertEqual(site.assignment_numbers, [2, 3, 10])
            self.assertIn('a%20%26%20b.csv', site.by_path['Assignment-3/data/a & b.csv']['url'])

    def test_untracked_assignment_stays_out_of_pages_search_and_archives(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root, {'Assignment-1/brief.pdf': '%PDF-released', 'Assignment-2/secret.pdf': 'Unreleased document'})
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            subprocess.run(['git', '-C', str(root), 'add', 'Assignment-1'], check=True)
            site = Site(root, root / 'preview')
            site.build()
            self.assertEqual(site.assignment_numbers, [1])
            for page in site.out.rglob('*.html'):
                text = page.read_text()
                self.assertNotIn('Assignment-2/secret.pdf', text)
                self.assertNotIn('assignments/assignment-2.html', text)
                self.assertNotIn('Unreleased title', text)
            self.assertFalse((site.out / 'bundles/Assignment-2.zip').exists())
            with zipfile.ZipFile(site.out / 'bundles/Assignment-1.zip') as archive:
                self.assertEqual(archive.read('Assignment-1/brief.pdf'), b'%PDF-released')
                self.assertIn('READ_ASSIGNMENT.txt', archive.namelist())
                self.assertNotIn('RUN_LESSON.txt', archive.namelist())

    def test_context_search_and_starter_navigation_stay_in_assignment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            site = self.fixture(root, {
                'Assignment-1/brief.pdf': '%PDF-1',
                'Assignment-1/01_start.py': 'print("a")',
                'Assignment-1/02_continue.py': 'print("b")',
                'Assignment-3/README.md': '# Assignment 3: Work with functions\n',
                'Assignment-3/start.py': 'print("c")',
                'first_file.py': 'print("hello")',
            })
            site.build()
            page = (site.out / 'view/Assignment-1/02_continue.py.html').read_text()
            self.assertIn('aria-current="page">', page)
            self.assertIn('Back to Assignment 1', page)
            pager = page.split('aria-label="More examples">')[1].split('</nav>')[0]
            self.assertNotIn('Assignment-3', pager)
            self.assertNotIn('first_file.py', pager)
            self.assertEqual(site.assignment_info(3)['title'], 'Work with functions')
            index = (site.out / 'index.html').read_text()
            data = json.loads(index.split('id="search-data">')[1].split('</script>')[0])
            pdf = next(item for item in data if item['path'] == 'Assignment-1/brief.pdf')
            self.assertEqual(pdf['assignment'], 1)
            self.assertIn('square numbers', pdf['search'])
            resources = (site.out / 'resources.html').read_text()
            self.assertNotIn('view/Assignment-', resources)
            self.assertIn('Open Assignments', resources)

    def test_empty_catalog_and_future_readme_folder_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            site = self.fixture(root, {})
            site.assignments()
            self.assertIn('No assignments have been released yet', (site.out / 'assignments.html').read_text())
            folder = root / 'Assignment-3'; folder.mkdir()
            (folder / 'README.md').write_text('# Assignment 3: Functions\n')
            site = Site(root, root / 'preview')
            site.assignments()
            page = (site.out / 'assignments/assignment-3.html').read_text()
            self.assertIn('Read brief', page)
            self.assertNotIn('DC Connect', page)
            rendered = site.markdown('[Next assignment](../Assignment-3/)', 'Assignment-1/README.md', 'view/Assignment-1/README.md.html')
            self.assertIn('assignments/assignment-3.html', rendered)


if __name__ == '__main__':
    unittest.main()
