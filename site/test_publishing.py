"""Recovery must repair transient failures without publishing stale or unapproved work."""
import json
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from publishing import inventory_matches, recover, recovery_plan, verify

REPOSITORY = 'Sohaib-Mohiuddin/cosc110005-f26'
SHA = 'a' * 40
NOW = datetime(2026, 11, 9, 20, tzinfo=timezone.utc)


def run(number=1, age=5, **changes):
    date = (NOW - timedelta(minutes=age)).isoformat()
    return {'id': number, 'head_sha': SHA, 'head_branch': 'main', 'event': 'push',
            'head_repository': {'full_name': REPOSITORY}, 'status': 'completed',
            'conclusion': 'failure', 'created_at': date, 'updated_at': date, **changes}


class Response:
    status = 204

    def __init__(self, text=''):
        self.text = text

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def read(self):
        return self.text.encode()


class PublishingTests(unittest.TestCase):
    def plan(self, runs, jobs=()):
        return recovery_plan(runs, jobs, SHA, REPOSITORY, NOW)[0]

    def test_workflow_level_errors_and_missing_deploy_jobs_can_recover(self):
        self.assertTrue(self.plan([run()], []))
        self.assertTrue(self.plan([run()], [{'name': 'build', 'conclusion': 'success', 'steps': []}]))
        self.assertTrue(self.plan([]))

    def test_active_runs_and_successful_deployment_propagation_are_left_alone(self):
        for status in ['queued', 'in_progress', 'waiting', 'requested', 'pending']:
            self.assertFalse(self.plan([run(status=status)]), status)
        self.assertFalse(self.plan([run(conclusion='success')]))
        self.assertTrue(self.plan([run(age=20, conclusion='success')]))
        self.assertFalse(self.plan([run(conclusion='action_required')]))

    def test_bounded_retries_resume_after_an_infrastructure_outage(self):
        runs = [run(number) for number in range(1, 4)]
        self.assertFalse(self.plan(runs))
        self.assertTrue(self.plan([run(number, age=65) for number in range(1, 4)]))

    def test_permanent_validation_failures_stop_after_three_runs(self):
        jobs = [{'name': 'build', 'steps': [{'name': 'Verify the student practice flow', 'conclusion': 'failure'}]}]
        self.assertTrue(self.plan([run()], jobs))
        self.assertFalse(self.plan([run(number, age=65) for number in range(1, 4)], jobs))

    def test_untrusted_and_old_runs_do_not_control_main_recovery(self):
        runs = [run(1, head_sha='b' * 40, status='in_progress'),
                run(2, head_branch='feature', status='in_progress'),
                run(3, event='pull_request', status='in_progress'),
                run(4, head_repository={'full_name': 'someone/fork'}, status='in_progress')]
        self.assertTrue(self.plan(runs))

    def test_published_inventory_requires_exact_commit_and_all_released_paths(self):
        paths = ['week-9-demos/main.py', 'week-9-demos/README.md']
        data = {'source_commit': SHA, 'materials': [{'path': path} for path in paths]}
        self.assertTrue(inventory_matches(data, SHA, paths))
        self.assertFalse(inventory_matches(data, 'b' * 40, paths))
        self.assertFalse(inventory_matches(data, SHA, paths + ['week-10-demos/main.py']))
        self.assertFalse(inventory_matches({'source_commit': SHA, 'materials': [{'path': paths[0]}] * 2}, SHA, paths))

    @patch('publishing.urlopen')
    @patch('publishing.published_sha', return_value=None)
    @patch('publishing.get_json')
    def test_workflow_without_jobs_uses_fresh_dispatch_not_unsupported_rerun(self, get, published, request):
        get.side_effect = [{'object': {'sha': SHA}}, {'workflow_runs': [run()]}, {'jobs': []}, {'object': {'sha': SHA}}]
        request.return_value = Response()
        self.assertIn('Requested', recover(REPOSITORY, 'test-token', 'https://example.org/course/', NOW))
        sent = request.call_args.args[0]
        self.assertTrue(sent.full_url.endswith('/actions/workflows/pages.yml/dispatches'))
        self.assertEqual(json.loads(sent.data), {'ref': 'main'})
        self.assertEqual(sent.method, 'POST')

    @patch('publishing.urlopen')
    @patch('publishing.published_sha', return_value=SHA)
    @patch('publishing.get_json', side_effect=[{'object': {'sha': SHA}}, {'workflow_runs': []}])
    def test_already_live_main_never_dispatches(self, get, published, request):
        self.assertIn('already live', recover(REPOSITORY, 'test-token', 'https://example.org/course/', NOW))
        request.assert_not_called()

    @patch('publishing.urlopen', return_value=Response())
    @patch('publishing.published_sha', return_value=SHA)
    @patch('publishing.get_json')
    def test_failed_live_verification_is_not_masked_by_a_current_commit_marker(self, get, published, request):
        get.side_effect = [{'object': {'sha': SHA}}, {'workflow_runs': [run()]},
                           {'jobs': [{'name': 'deploy', 'conclusion': 'failure', 'steps': []}]}, {'object': {'sha': SHA}}]
        self.assertIn('Requested', recover(REPOSITORY, 'test-token', 'https://example.org/course/', NOW))
        request.assert_called_once()

    @patch('publishing.urlopen')
    @patch('publishing.published_sha', return_value=None)
    @patch('publishing.get_json')
    def test_main_advancing_during_recovery_prevents_old_dispatch(self, get, published, request):
        get.side_effect = [{'object': {'sha': SHA}}, {'workflow_runs': [run()]}, {'jobs': []}, {'object': {'sha': 'b' * 40}}]
        self.assertIn('advanced', recover(REPOSITORY, 'test-token', 'https://example.org/course/', NOW))
        request.assert_not_called()

    @patch('build.discover', return_value=[{'path': 'week-12-demos/a & b.py', 'url': 'view/week-12-demos/a%20%26%20b.py.html', 'week': 12}])
    @patch('publishing.get_json', return_value={'source_commit': SHA, 'materials': [{'path': 'week-12-demos/a & b.py'}]})
    @patch('publishing.urlopen')
    def test_live_verification_checks_newest_week_and_project_relative_links(self, request, get, discover):
        request.side_effect = [Response('<a href="weeks/week-12.html">Week 12</a>'),
                               Response('<a href="../view/week-12-demos/a%20%26%20b.py.html">Demo</a>')]
        self.assertIn('latest week 12', verify('https://example.org/course/', SHA, attempts=1))

    @patch('build.discover', return_value=[{'path': 'week-12-demos/main.py', 'url': 'view/week-12-demos/main.py.html', 'week': 12}])
    @patch('publishing.get_json', return_value={'source_commit': SHA, 'materials': [{'path': 'week-12-demos/main.py'}]})
    @patch('publishing.urlopen', return_value=Response('<a href="weeks/week-11.html">Old week</a>'))
    def test_live_verification_rejects_a_stale_homepage_even_with_new_inventory(self, request, get, discover):
        with self.assertRaisesRegex(RuntimeError, 'missing released lesson links'):
            verify('https://example.org/course/', SHA, attempts=1)


if __name__ == '__main__':
    unittest.main()
