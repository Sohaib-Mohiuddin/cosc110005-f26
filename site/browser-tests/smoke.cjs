/* Real browser + real Pyodide checks. Run after python site/build.py. */
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert = require('node:assert/strict');
const path = require('node:path');
const {spawn} = require('node:child_process');

(async () => {
  let server;
  let browser;
  try {
    let base = process.env.SITE_BASE_URL;
    if (!base) {
      const output = process.env.SITE_OUTPUT || path.resolve(__dirname, '../../_site');
      server = spawn('python3', ['-u', '-c', `
import http.server, sys
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=sys.argv[1], **kwargs)
    def do_GET(self):
        if not self.path.startswith('/cosc110005-f26/'):
            self.send_error(404); return
        self.path = self.path[len('/cosc110005-f26'):]
        super().do_GET()
    def log_message(self, *args): pass
server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
print(server.server_port, flush=True)
server.serve_forever()
`, output], {stdio: ['ignore', 'pipe', 'pipe']});
      const port = await new Promise((resolve, reject) => {
        server.stdout.once('data', data => resolve(Number(data.toString().trim())));
        server.once('error', reject);
        server.once('exit', code => reject(new Error(`Preview exited: ${code}`)));
      });
      base = `http://127.0.0.1:${port}/cosc110005-f26/`;
    }
    browser = await chromium.launch({headless: true, ...(process.env.BROWSER_EXECUTABLE ? {executablePath: process.env.BROWSER_EXECUTABLE} : {})});
    const context = await browser.newContext({viewport: {width: 1440, height: 1000}, acceptDownloads: true});
    const page = await context.newPage();
    page.setDefaultTimeout(15000);
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    async function lesson(relative) {
      await page.goto(base + 'view/' + relative + '.html');
      await page.locator('#python-runner > summary').click();
    }
    async function run(code, input = '') {
      await page.locator('#python-editor').fill(code);
      await page.locator('#python-input').fill(input);
      await page.locator('#run-python').click();
      await page.waitForFunction(() => !document.querySelector('#run-python').disabled, {}, {timeout: 90000});
      return page.locator('#python-output').textContent();
    }
    await page.goto(base);
    assert(await page.locator('.current-week').isVisible());
    await page.getByLabel('Filter by week', {exact: true}).selectOption('6');
    await page.getByLabel('Filter by file type', {exact: true}).selectOption('PY');
    await page.getByLabel('Search all course materials').fill('while');
    assert(await page.locator('#search-results mark').count() > 0);
    assert((await page.locator('#search-results .file-row small').allTextContents()).some(text => text.includes('week-6-demos')));
    assert(page.url().includes('week=6'));
    await page.reload();
    assert.equal(await page.locator('#material-week').inputValue(), '6');
    await page.getByRole('button', {name: 'Clear search'}).click();
    assert(await page.locator('#browse-content').isVisible());
    console.log('PASS: week/type/keyword search, highlighted excerpts, URL restoration, clear.');

    // Runtime must not download merely by reading or expanding an example.
    let runtimeRequests = 0;
    context.on('request', request => { if (request.url().includes('/pyodide/')) runtimeRequests++; });
    await lesson('week-3-demos/01_explore_data_types.py');
    assert.equal(runtimeRequests, 0);
    const output = await run('name = input("Name: ")\nage = int(input("Age: "))\nprint(f"Hello {name}, next year {age + 1}")', 'Sam\n18\n');
    assert(output.includes('Hello Sam, next year 19'), output);
    assert(runtimeRequests > 0);
    assert.equal(await page.locator('#runner-status').textContent(), 'Run complete.');
    await page.reload();
    await page.locator('#python-runner > summary').click();
    assert((await page.locator('#python-editor').inputValue()).includes('Hello {name}'));
    const downloaded = page.waitForEvent('download');
    await page.getByRole('button', {name: 'Download my code'}).click();
    const download = await downloaded;
    assert.equal(download.suggestedFilename(), '01_explore_data_types.py');
    const parts = [];
    for await (const part of await download.createReadStream()) parts.push(part);
    assert(Buffer.concat(parts).toString().includes('Hello {name}'));
    assert((await run('print("<script>window.bad = true</script>")')).includes('<script>'));
    assert.equal(await page.evaluate(() => window.bad), undefined);
    assert((await run('input("One: ")\ninput("Two: ")', 'one\n')).includes('Add the missing answers'));
    const traceback = await run('raise ValueError("try again")');
    assert(traceback.includes('ValueError: try again') && traceback.includes('raise ValueError("try again")'), traceback);
    await run('remember = 42\nprint(remember)');
    assert((await run('print("fresh", "remember" not in globals())')).includes('fresh True'));
    assert((await run('while True:\n    print("x" * 4096)')).includes('Output limit'));
    const infinite = await run('while True:\n    pass');
    assert(infinite.includes('Stopped after 10 seconds'), infinite);
    await page.locator('#python-editor').fill('while True:\n    pass');
    await page.locator('#run-python').click();
    await page.locator('#stop-python').click();
    await page.waitForFunction(() => !document.querySelector('#run-python').disabled);
    assert.equal(await page.locator('#runner-status').textContent(), 'Stopped.');
    assert((await run('print("recovered")')).includes('recovered'));
    console.log('PASS: real Python, queued input, saved edits, downloads, escaped output, errors, fresh runs, output/time limits, Stop and recovery.');

    await lesson('Midterm%20Preparation/06_estimate_printing_cost.py');
    await page.locator('#check-python').click();
    await page.waitForFunction(() => !document.querySelector('#check-python').disabled, {}, {timeout: 90000});
    assert((await page.locator('#runner-status').textContent()).includes('0 of 2'));
    await page.locator('#python-editor').fill('pages = int(input())\ncopies = int(input())\nprice = float(input())\nprint(pages * copies)\nprint(f"${pages * copies * price:.2f}")');
    await page.locator('#check-python').click();
    await page.waitForFunction(() => !document.querySelector('#check-python').disabled, {}, {timeout: 90000});
    assert((await page.locator('#runner-status').textContent()).includes('2 of 2'));
    await lesson('Midterm%20Preparation/01_plan_a_picnic_budget.py');
    await page.locator('#python-editor').fill('headcount = 9\nprint("$45.00")\nprint(f"${45 / headcount:.2f}")');
    await page.locator('#check-python').click();
    await page.waitForFunction(() => !document.querySelector('#check-python').disabled, {}, {timeout: 90000});
    assert((await page.locator('#runner-status').textContent()).includes('2 of 2'));
    assert((await page.locator('#python-editor').inputValue()).includes('headcount = 9'));
    await page.locator('#lesson-complete').check();
    await page.goto(base);
    assert((await page.locator('#resume-practice').textContent()).includes('1 of'));
    await page.locator('#resume-practice a').click();
    assert(await page.locator('#lesson-complete').isChecked());
    console.log('PASS: incomplete starters fail, completed practice passes, per-case variable substitution, progress and resume.');

    await page.getByLabel('Code size', {exact: true}).selectOption('18');
    await page.getByLabel('Wrap long lines', {exact: true}).check();
    await page.reload();
    assert.equal(await page.locator('#code-size').inputValue(), '18');
    assert(await page.locator('#code-wrap').isChecked());
    assert.equal(await page.locator('.source pre').evaluate(el => getComputedStyle(el).fontSize), '18px');
    await page.setViewportSize({width: 390, height: 844});
    await page.locator('#python-runner > summary').click();
    await page.locator('#python-editor').focus();
    await page.keyboard.press('Tab');
    assert(await page.locator('#python-input').evaluate(el => el === document.activeElement));
    assert((await run('print("mobile works")')).includes('mobile works'));
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    assert(await page.locator('.source pre').evaluate(el => el.scrollWidth <= el.clientWidth));
    await page.getByRole('button', {name: 'Toggle navigation'}).click();
    assert.equal(await page.locator('.sidebar').evaluate(el => el.inert), false);
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('.sidebar').evaluate(el => el.inert), true);
    page.once('dialog', dialog => dialog.accept());
    await page.getByRole('button', {name: 'Reset code'}).click();
    assert((await page.locator('#python-editor').inputValue()).includes('sandwich_count = 12'));
    await page.evaluate(() => {document.activeElement.blur(); window.scrollTo(0, 0);});
    if (process.env.SCREENSHOT_DIR) await page.screenshot({path: path.join(process.env.SCREENSHOT_DIR, 'course-mobile.png'), fullPage: true});
    await page.setViewportSize({width: 1440, height: 1000});
    await page.evaluate(() => window.scrollTo(0, 0));
    if (process.env.SCREENSHOT_DIR) await page.screenshot({path: path.join(process.env.SCREENSHOT_DIR, 'course-desktop.png'), fullPage: true});
    console.log('PASS: saved reading settings, mobile execution/layout, keyboard navigation, Reset.');

    const nojs = await browser.newContext({javaScriptEnabled: false, viewport: {width: 390, height: 844}});
    const staticPage = await nojs.newPage();
    await staticPage.goto(base + 'view/week-3-demos/01_explore_data_types.py.html');
    assert(await staticPage.locator('#source-code').isVisible());
    assert(!(await staticPage.locator('#python-runner').isVisible()));
    const bundle = await staticPage.getByRole('link', {name: 'Download complete lesson ZIP'}).getAttribute('href');
    const response = await staticPage.request.get(new URL(bundle, staticPage.url()).href);
    assert.equal(response.status(), 200);
    assert((await response.body()).subarray(0, 2).equals(Buffer.from('PK')));
    const blocked = await browser.newContext();
    await blocked.addInitScript(() => { Object.defineProperty(window, 'localStorage', {get() { throw new Error('Blocked'); }}); });
    const blockedPage = await blocked.newPage();
    await blockedPage.goto(base + 'view/week-3-demos/01_explore_data_types.py.html');
    await blockedPage.locator('#python-runner > summary').click();
    assert((await blockedPage.locator('#save-status').textContent()).includes('unavailable'));
    await blockedPage.locator('#python-editor').fill('print("unsaved but runnable")');
    await blockedPage.locator('#run-python').click();
    await blockedPage.waitForFunction(() => !document.querySelector('#run-python').disabled, {}, {timeout: 90000});
    assert((await blockedPage.locator('#python-output').textContent()).includes('unsaved but runnable'));
    const unavailable = await browser.newContext();
    await unavailable.route('**/assets/python-worker.mjs', route => route.abort());
    const unavailablePage = await unavailable.newPage();
    await unavailablePage.goto(base + 'view/week-3-demos/01_explore_data_types.py.html');
    await unavailablePage.locator('#python-runner > summary').click();
    await unavailablePage.locator('#run-python').click();
    await unavailablePage.waitForFunction(() => !document.querySelector('#run-python').disabled);
    assert((await unavailablePage.locator('#python-output').textContent()).includes('Python could not start'));
    assert(await unavailablePage.locator('#source-code').isVisible());
    const imported = await page.evaluate(baseURL => new Promise((resolve, reject) => {
      const worker = new Worker(new URL('assets/python-worker.mjs', baseURL), {type: 'module'});
      let text = '';
      const timer = setTimeout(() => {worker.terminate(); reject(new Error('Dependency fixture timed out'));}, 60000);
      worker.onmessage = ({data}) => {
        if (data.type === 'output') text += data.text;
        if (data.type === 'done' || data.type === 'error') {
          clearTimeout(timer); worker.terminate();
          if (data.type === 'error') reject(new Error(data.text)); else resolve(text);
        }
      };
      const fixtures = [['fixture lesson/helper.py', 'def double(n): return n * 2'], ['fixture lesson/data.csv', '21'], ['other-week/shared_rule.py', 'VALUE = 7']];
      worker.postMessage({path: 'fixture lesson/demo.py', stdin: '', code: 'from helper import double\nfrom shared_rule import VALUE\nfrom pathlib import Path\nprint(double(int(Path("data.csv").read_text())))\nprint(VALUE, __name__, Path(__file__).name)\nimport unittest\nclass Example(unittest.TestCase):\n    def test_double(self): self.assertEqual(double(3), 6)\nunittest.main()', files: fixtures.map(([path, source]) => ({path, bytes: new TextEncoder().encode(source).buffer}))});
    }), base);
    assert(imported.includes('42') && imported.includes('7 __main__ demo.py'), imported);
    assert(imported.includes('Ran 1 test') && imported.includes('OK'), imported);
    assert.deepEqual(errors, []);
    console.log('PASS: no-JavaScript source/downloads, complete ZIP, blocked storage/runtime fallback, companion imports/data/files with spaces, no uncaught page errors.');
  } finally {
    await browser?.close();
    server?.kill();
  }
})().catch(error => {console.error(error); process.exitCode = 1;});
