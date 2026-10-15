"""Regression checks for release boundaries, complete bundles, and runner manifests."""
import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

from build import ROOT, Site, discover
from learning import json_script


class LearningTests(unittest.TestCase):
    def fixture(self, root):
        (root / 'site').mkdir()
        (root / 'site/course.json').write_text((ROOT / 'site/course.json').read_text())

    def test_untracked_lessons_never_enter_default_build(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            for week in [6, 7]:
                folder = root / f'week-{week}-demos'
                folder.mkdir()
                (folder / '01_example.py').write_text(f'print("week {week}")')
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            subprocess.run(['git', '-C', str(root), 'add', 'week-6-demos'], check=True)
            site = Site(root, root / 'preview')
            self.assertEqual(site.weeks, [6])
            self.assertEqual(len(discover(root, include_untracked=True)), 2)
            site.out.mkdir()
            site.learning.build_bundles()
            site.home()
            page = (site.out / 'index.html').read_text()
            self.assertNotIn('week-7', page)
            self.assertIn('This week · Week 6', page)
            self.assertFalse((site.out / 'bundles/week-7-demos.zip').exists())
            with zipfile.ZipFile(site.out / 'bundles/week-6-demos.zip') as archive:
                self.assertFalse(any('week-7' in name for name in archive.namelist()))

    def test_bundles_and_runner_preserve_imported_module_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            for path, text in {
                'week-9-demos/01_demo.py': 'from helper import answer\nprint(answer)',
                'week-9-demos/data.csv': 'value\n42\n',
                'week-8-demos/helper.py': 'answer = 42',
                'week-9-demos/02_gui.py': 'import tkinter',
            }.items():
                target = root / path; target.parent.mkdir(exist_ok=True); target.write_text(text)
            site = Site(root, root / 'preview')
            demo = site.by_path['week-9-demos/01_demo.py']
            self.assertEqual(site.learning.desktop_reason(demo), '')
            self.assertIn('tkinter', site.learning.desktop_reason(site.by_path['week-9-demos/02_gui.py']))
            controls = site.learning.controls(demo)
            data = json.loads(controls.split('id="runner-data">')[1].split('</script>')[0])
            self.assertIn('week-8-demos/helper.py', [item['path'] for item in data['files']])
            site.out.mkdir()
            site.learning.build_bundles()
            with zipfile.ZipFile(site.out / 'bundles/week-9-demos.zip') as archive:
                self.assertEqual(archive.read('week-8-demos/helper.py'), b'answer = 42')
                self.assertEqual(archive.read('week-9-demos/data.csv'), b'value\n42\n')

    def test_runner_json_cannot_end_script(self):
        value = {'source': '</script><script>alert("x")</script>&'}
        encoded = json_script(value)
        self.assertNotIn('<', encoded)
        self.assertEqual(json.loads(encoded), value)

    def test_midterm_cases_cover_all_starters_without_solutions(self):
        cases = json.loads((ROOT / 'site/practice_cases.json').read_text())
        starters = {path.relative_to(ROOT).as_posix() for path in (ROOT / 'Midterm Preparation').glob('*.py')}
        self.assertEqual(set(cases), starters)
        for path, entry in cases.items():
            self.assertTrue(entry['cases'], path)
            for case in entry['cases']:
                self.assertIsInstance(case['stdin'], str)
                self.assertTrue(case['contains'])
                self.assertTrue(all(isinstance(part, str) and part for part in case['contains']))
                self.assertNotIn('code', case)

    def test_desktop_programs_have_no_run_button(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.fixture(root)
            (root / 'gui.py').write_text('import tkinter\n')
            site = Site(root, root / 'preview')
            site.viewer(site.files[0])
            page = (site.out / 'view/gui.py.html').read_text()
            self.assertIn('Requires desktop Python', page)
            self.assertNotIn('id="run-python"', page)
            self.assertIn('Download complete lesson ZIP', page)


if __name__ == '__main__':
    unittest.main()
