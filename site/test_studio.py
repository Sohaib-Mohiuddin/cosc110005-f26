"""Student platform gates: authored activities, offline completeness, release scope."""
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

from build import ROOT, Site


class StudioTests(unittest.TestCase):
    def fixture(self, root):
        (root / 'site').mkdir()
        for name in ['course.json', 'concepts.json', 'activities.json', 'reference.json']:
            shutil.copyfile(ROOT / 'site' / name, root / 'site' / name)
        shutil.copytree(ROOT / 'site/assets', root / 'site/assets', ignore=shutil.ignore_patterns('__pycache__'))

    def test_offline_and_study_data_use_only_released_materials(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.fixture(root)
            for name, source in {'week-3-demos/01_data.py': 'print(42)', 'week-8-demos/private.py': 'private_contents_not_for_students', 'Assignment-2/brief.md': '# Private assignment title'}.items():
                path = root / name; path.parent.mkdir(exist_ok=True); path.write_text(source)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            subprocess.run(['git', '-C', str(root), 'add', 'week-3-demos'], check=True)
            site = Site(root, root / 'output'); site.build()
            data = json.loads((site.out / 'study-data.json').read_text())
            self.assertEqual([item['path'] for item in data['materials']], ['week-3-demos/01_data.py'])
            self.assertTrue(all(topic['week'] <= 3 for topic in data['topics']))
            for path in [site.out / 'study-data.json', site.out / 'offline-manifest.json', site.out / 'updates.html']:
                text = path.read_text()
                self.assertNotIn('week-8-demos', text)
                self.assertNotIn('Assignment-2', text)
                self.assertNotIn('private_contents', text)

    def test_every_offline_pack_and_shell_url_exists(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Site(ROOT, Path(directory)); site.build()
            manifest = json.loads((site.out / 'offline-manifest.json').read_text())
            self.assertTrue(manifest['packs'])
            for url in manifest['shell'] + [url for pack in manifest['packs'] for url in pack['urls']]:
                self.assertFalse(urlsplit(url).scheme)
                target = (site.out / unquote(url)).resolve()
                self.assertTrue(target.is_relative_to(site.out.resolve()))
                self.assertTrue(target.exists(), url)
                self.assertNotIn('__pycache__', url)
            worker = (site.out / 'service-worker.js').read_text()
            self.assertIn(manifest['version'], worker)
            self.assertNotIn('__COURSE_SHELL__', worker)

    def test_authored_activities_cover_all_four_formats(self):
        activities = json.loads((ROOT / 'site/activities.json').read_text())
        topics = {topic['id'] for topic in json.loads((ROOT / 'site/concepts.json').read_text())}
        self.assertEqual({item['type'] for item in activities}, {'predict', 'fill', 'arrange', 'debug'})
        self.assertEqual(len({item['id'] for item in activities}), len(activities))
        for activity in activities:
            self.assertIn(activity['topic'], topics)
            self.assertTrue(activity['hints'])
            self.assertTrue(activity['explanation'])
            if activity['type'] == 'arrange':
                self.assertEqual(set(activity['solution']), {block['id'] for block in activity['blocks']})
            elif activity['type'] == 'fill':
                self.assertEqual(activity['code'].count('___'), 1)
            elif activity['type'] == 'predict':
                result = subprocess.run(['python3', '-c', activity['code']], capture_output=True, text=True, timeout=3)
                self.assertEqual(result.returncode, 0)
                self.assertEqual(result.stdout.strip(), activity['answer'].strip())

    def test_readable_assignment_includes_both_example_transcripts(self):
        text = (ROOT / 'Assignment-1/brief.md').read_text()
        for required in ['Chicken', '10001', '4 (2 squared)', '100 (10 squared)', 'Academic integrity', 'DC Connect']:
            self.assertIn(required, text)


if __name__ == '__main__':
    unittest.main()
