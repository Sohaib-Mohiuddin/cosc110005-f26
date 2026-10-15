(() => {
  const panel = document.querySelector('#python-runner');
  if (!panel) return;
  const data = JSON.parse(document.querySelector('#runner-data').textContent);
  const editor = document.querySelector('#python-editor');
  const input = document.querySelector('#python-input');
  const output = document.querySelector('#python-output');
  const status = document.querySelector('#runner-status');
  const saveStatus = document.querySelector('#save-status');
  const run = document.querySelector('#run-python');
  const stop = document.querySelector('#stop-python');
  const reset = document.querySelector('#reset-python');
  const check = document.querySelector('#check-python');
  const results = document.querySelector('#check-results');
  const original = document.querySelector('#source-code').textContent;
  const base = new URL(document.body.dataset.root, location.href);
  const storageKey = `cosc-practice:${base.pathname}:${data.path}`;
  let busy = false;
  let cancel = null;
  let cancelled = false;
  let filesPromise;
  let saveTimer;
  panel.hidden = false;
  editor.value = original;
  input.value = data.cases[0]?.stdin || '';
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey));
    if (saved && typeof saved.code === 'string') {
      editor.value = saved.code;
      input.value = typeof saved.stdin === 'string' ? saved.stdin : '';
      saveStatus.textContent = saved.original !== original ? 'Restored your copy. The course example has changed; Reset code loads the updated original.' : 'Restored your saved copy from this browser.';
    }
  } catch { saveStatus.textContent = 'Browser saving is unavailable. Download your code to keep it.'; }
  function save() {
    clearTimeout(saveTimer);
    try {
      localStorage.setItem(storageKey, JSON.stringify({code: editor.value, stdin: input.value, original}));
      saveStatus.textContent = 'Saved on this browser. Download a copy to use another device.';
    } catch { saveStatus.textContent = 'Could not save in this browser. Download your code to keep it.'; }
  }
  for (const control of [editor, input]) control.addEventListener('input', () => {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(save, 300);
  });
  window.addEventListener('pagehide', save);
  function setBusy(value) {
    busy = value;
    run.disabled = value;
    reset.disabled = value;
    if (check) check.disabled = value;
    stop.disabled = !value;
    panel.setAttribute('aria-busy', String(value));
  }
  async function loadFiles() {
    if (!filesPromise) {
      filesPromise = Promise.all(data.files.map(async file => {
        const response = await fetch(file.url, {signal: AbortSignal.timeout(30000)});
        if (!response.ok) throw new Error(`Could not load ${file.path}. Download the lesson ZIP or retry.`);
        return {path: file.path, bytes: await response.arrayBuffer()};
      })).catch(error => { filesPromise = null; throw error; });
    }
    return filesPromise;
  }
  function execute(code, stdin, overrides) {
    return new Promise(resolve => {
      let worker;
      let text = '';
      let finished = false;
      let timer;
      function finish(error = '') {
        if (finished) return;
        finished = true;
        clearTimeout(timer);
        worker?.terminate();
        cancel = null;
        resolve({text, error});
      }
      cancel = () => finish('Stopped. Edit your code and run again.');
      status.textContent = 'Loading Python and lesson files… The first run may take a little longer.';
      timer = setTimeout(() => finish('Python could not load within 60 seconds. Check your connection and retry, or download the lesson.'), 60000);
      loadFiles().then(files => {
        if (finished) return;
        worker = new Worker(new URL('assets/python-worker.mjs', base), {type: 'module'});
        worker.onerror = event => { event.preventDefault(); finish('Python could not start. Check your connection and retry, or use desktop Python.'); };
        worker.onmessage = ({data: message}) => {
          if (finished) return;
          if (message.type === 'running') {
            clearTimeout(timer);
            timer = setTimeout(() => finish('Stopped after 10 seconds. Check loop conditions and stop values, then try again.'), 10000);
            status.textContent = 'Running…';
          } else if (message.type === 'output') {
            if (text.length + message.text.length > 65536) return finish('Output limit reached (64 KB). Reduce printing and try again.');
            text += message.text;
            output.textContent = text;
          } else if (message.type === 'done') finish();
          else if (message.type === 'error') finish(message.text);
        };
        worker.postMessage({code, stdin, overrides, path: data.path, files});
      }).catch(error => finish(error.message));
    });
  }
  function showError(error) {
    output.textContent += '\n' + error;
    if (error.includes('EOFError')) output.textContent += '\nAdd the missing answers to Program input, one per line, then run again.';
  }
  async function start(checking = false) {
    if (busy) return;
    save();
    cancelled = false;
    setBusy(true);
    output.textContent = '';
    if (results) results.replaceChildren();
    const code = editor.value;
    try {
      if (!checking) {
        const result = await execute(code, input.value, {});
        if (result.error) showError(result.error);
        status.textContent = result.error ? (cancelled ? 'Stopped.' : 'Run finished with an error. See Output.') : 'Run complete.';
      } else {
        let passed = 0;
        for (const [index, sample] of data.cases.entries()) {
          if (cancelled) break;
          output.textContent = '';
          const result = await execute(code, sample.stdin || '', sample.overrides || {});
          const missing = sample.contains.filter(value => !result.text.includes(value));
          const ok = !result.error && !missing.length;
          if (ok) passed++;
          const row = document.createElement('li');
          row.className = ok ? 'check-pass' : 'check-fail';
          row.textContent = `Case ${index + 1}${sample.label ? ': ' + sample.label : ''} — ${ok ? 'Passed' : result.error ? 'Could not complete' : 'Expected output missing: ' + missing.join(', ')}`;
          const details = document.createElement('details');
          const summary = document.createElement('summary'); summary.textContent = 'Actual output';
          const actual = document.createElement('pre'); actual.textContent = result.text + (result.error ? '\n' + result.error : '') || '(no output)';
          details.append(summary, actual); row.append(details); results.append(row);
          if (result.error) showError(result.error);
        }
        status.textContent = cancelled ? 'Checks stopped.' : `${passed} of ${data.cases.length} sample checks passed. Review the requirements too; these checks are not a grade.`;
      }
    } finally { setBusy(false); }
  }
  run.addEventListener('click', () => start());
  check?.addEventListener('click', () => start(true));
  stop.addEventListener('click', () => { cancelled = true; cancel?.(); });
  reset.addEventListener('click', () => {
    if (!window.confirm('Replace your saved edits with the original course code? Download your code first if you want to keep it.')) return;
    editor.value = original;
    input.value = data.cases[0]?.stdin || '';
    output.textContent = '';
    results?.replaceChildren();
    status.textContent = 'Original code restored.';
    save();
    editor.focus();
    editor.setSelectionRange(0, 0);
    editor.scrollTop = 0;
  });
  document.querySelector('#download-python').addEventListener('click', () => {
    save();
    const url = URL.createObjectURL(new Blob([editor.value], {type: 'text/x-python;charset=utf-8'}));
    const link = document.createElement('a');
    link.href = url; link.download = data.path.split('/').pop();
    link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  editor.addEventListener('keydown', event => {
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') { event.preventDefault(); start(); }
  });
})();
