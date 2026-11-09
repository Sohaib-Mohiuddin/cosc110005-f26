"""Verify published course content and recover stalled GitHub Pages releases."""
import argparse
import json
import os
import re
import time
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = 'pages.yml'
MAX_RUNS_PER_HOUR = 3
VALIDATION_STEPS = {'Check discovery, source previews, and all local links',
                    'Build the course library', 'Verify the student practice flow'}


def timestamp(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def recovery_plan(runs, jobs, sha, repository, now):
    """Only trusted runs for the current main commit can request another publish."""
    runs = [run for run in runs if run['head_sha'] == sha and run['head_branch'] == 'main'
            and run['event'] in {'push', 'workflow_dispatch'}
            and run.get('head_repository', {}).get('full_name') == repository]
    runs.sort(key=lambda run: run['id'], reverse=True)
    if any(run['status'] != 'completed' for run in runs):
        return False, 'A publication for current main is already running.'
    if runs and runs[0]['conclusion'] not in {'failure', 'timed_out', 'cancelled', 'success'}:
        return False, 'The latest run requires inspection or approval: ' + str(runs[0]['conclusion'])
    if runs and runs[0]['conclusion'] == 'success' and now - timestamp(runs[0]['updated_at']) < timedelta(minutes=10):
        return False, 'Allow the successful deployment time to propagate.'
    validation_failed = any(step.get('conclusion') == 'failure' and step['name'] in VALIDATION_STEPS
                            for job in jobs for step in job.get('steps', []))
    if validation_failed and len(runs) >= MAX_RUNS_PER_HOUR:
        return False, 'Validation failed repeatedly. Fix the reported test; publishing gates remain required.'
    recent = [run for run in runs if timestamp(run['created_at']) > now - timedelta(hours=1)]
    if len(recent) >= MAX_RUNS_PER_HOUR:
        return False, 'Recovery is rate limited to three publication runs per commit per hour.'
    return True, 'The current main commit is not live; request a fresh publication.'


def get_json(url, token=None):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'course-pages-recovery'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers=headers), timeout=20) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code not in {429, 500, 502, 503, 504} or attempt == 2:
                raise
        except URLError:
            if attempt == 2:
                raise
        time.sleep(2 ** (attempt + 1))


def study_url(base, sha):
    if not base.endswith('/'):
        base += '/'
    return urljoin(base, 'study-data.json') + '?release=' + quote(sha, safe='')


def published_sha(base, sha):
    try:
        return get_json(study_url(base, sha)).get('source_commit')
    except (HTTPError, URLError, ValueError):
        return None


def inventory_matches(data, sha, paths):
    actual = [item['path'] for item in data.get('materials', [])]
    return data.get('source_commit') == sha and len(actual) == len(paths) and set(actual) == set(paths)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a' and 'href' in dict(attrs):
            self.hrefs.append(dict(attrs)['href'])


def verify(base, sha, attempts=8, delay=10):
    from build import discover
    materials = discover(ROOT)
    paths = [item['path'] for item in materials]
    latest = max((item['week'] for item in materials if item['week'] is not None), default=None)
    last_error = 'Publication did not match current main.'
    for attempt in range(attempts):
        try:
            data = get_json(study_url(base, sha))
            if not inventory_matches(data, sha, paths):
                raise ValueError('The live commit or released-material inventory is stale.')
            pages = ['index.html'] + ([f'weeks/week-{latest}.html'] if latest is not None else [])
            for page in pages:
                url = urljoin(base.rstrip('/') + '/', page)
                with urlopen(url + '?release=' + sha, timeout=20) as response:
                    parser = Links(); parser.feed(response.read().decode('utf-8'))
                targets = {urljoin(url, href) for href in parser.hrefs}
                if page == 'index.html':
                    expected = [urljoin(base.rstrip('/') + '/', f'weeks/week-{latest}.html')] if latest is not None else []
                else:
                    expected = [urljoin(base.rstrip('/') + '/', item['url']) for item in materials if item['week'] == latest]
                if any(target not in targets for target in expected):
                    raise ValueError('The live page is missing released lesson links: ' + page)
            return f'Live commit {sha[:7]} verified: {len(paths)} released materials; latest week {latest}.'
        except (HTTPError, URLError, ValueError, KeyError) as error:
            last_error = str(error)
            if attempt + 1 < attempts:
                time.sleep(delay)
    raise RuntimeError(last_error)


def recover(repository, token, base, now=None):
    if not re.fullmatch(r'[\w.-]+/[\w.-]+', repository):
        raise ValueError('Expected owner/repository.')
    api = 'https://api.github.com/repos/' + repository
    sha = get_json(api + '/git/ref/heads/main', token)['object']['sha']
    live_sha = published_sha(base, sha)
    response = get_json(api + '/actions/workflows/' + WORKFLOW + '/runs?branch=main&head_sha=' + sha + '&per_page=100', token)
    runs = response['workflow_runs']
    trusted = [run for run in runs if run['head_sha'] == sha and run['head_branch'] == 'main'
               and run['event'] in {'push', 'workflow_dispatch'}
               and run.get('head_repository', {}).get('full_name') == repository]
    latest = max(trusted, key=lambda run: run['id'], default=None)
    if live_sha == sha and (latest is None or latest['conclusion'] == 'success'):
        return 'Current main is already live. No recovery needed.'
    jobs = []
    if latest and latest['status'] == 'completed':
        jobs = get_json(api + '/actions/runs/' + str(latest['id']) + '/jobs?filter=latest&per_page=100', token)['jobs']
    retry, reason = recovery_plan(runs, jobs, sha, repository, now or datetime.now(timezone.utc))
    if not retry:
        return reason
    if get_json(api + '/git/ref/heads/main', token)['object']['sha'] != sha:
        return 'Main advanced during recovery. The newer release takes priority.'
    # A workflow-level internal error may not have any re-runnable jobs. Dispatch
    # a fresh run instead. Never retry this POST blindly after an uncertain reply.
    request = Request(api + '/actions/workflows/' + WORKFLOW + '/dispatches', method='POST',
                      data=json.dumps({'ref': 'main'}).encode(),
                      headers={'Accept': 'application/vnd.github+json', 'Authorization': 'Bearer ' + token,
                               'Content-Type': 'application/json', 'User-Agent': 'course-pages-recovery'})
    with urlopen(request, timeout=20) as response:
        if response.status != 204:
            raise RuntimeError('GitHub did not accept the publication request.')
    return reason + ' Requested for ' + sha[:7] + '.'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['verify', 'recover'])
    args = parser.parse_args()
    repository = os.environ.get('GITHUB_REPOSITORY', 'Sohaib-Mohiuddin/cosc110005-f26')
    owner, name = repository.split('/', 1)
    base = os.environ.get('COURSE_SITE_URL') or f'https://{owner.lower()}.github.io/{name}/'
    if urlsplit(base).scheme != 'https':
        raise ValueError('The published course URL must use HTTPS.')
    if args.operation == 'verify':
        message = verify(base, os.environ['GITHUB_SHA'])
    else:
        token = os.environ.get('GH_TOKEN')
        if not token:
            raise ValueError('Recovery requires the workflow token with actions:write.')
        message = recover(repository, token, base)
    print(message)
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as summary:
            summary.write(message + '\n')


if __name__ == '__main__':
    main()
