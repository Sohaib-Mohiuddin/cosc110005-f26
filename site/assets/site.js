const menu = document.querySelector('.menu-toggle');
const sidebar = document.querySelector('.sidebar');
const mobileNavigation = window.matchMedia('(max-width: 800px)');
function syncNavigation() { sidebar.inert = mobileNavigation.matches && !sidebar.classList.contains('open'); }
function closeMenu() { sidebar.classList.remove('open'); menu?.setAttribute('aria-expanded', 'false'); syncNavigation(); }
menu?.addEventListener('click', () => {
  const open = sidebar.classList.toggle('open');
  menu.setAttribute('aria-expanded', String(open));
  syncNavigation();
});
mobileNavigation.addEventListener('change', syncNavigation);
syncNavigation();
document.addEventListener('keydown', event => { if (event.key === 'Escape' && sidebar.classList.contains('open')) { closeMenu(); menu?.focus(); } });
document.addEventListener('click', event => { if (!sidebar.contains(event.target) && !menu?.contains(event.target)) closeMenu(); });
sidebar.addEventListener('click', event => {
  if (event.target.closest('a')) closeMenu();
});

const copyButton = document.querySelector('[data-copy]');
copyButton?.addEventListener('click', async () => {
  const code = document.querySelector('#source-code').textContent;
  const status = document.querySelector('#copy-status');
  try {
    await navigator.clipboard.writeText(code);
    copyButton.textContent = 'Copied!';
    status.textContent = 'Code copied to your clipboard.';
    setTimeout(() => { copyButton.textContent = 'Copy code'; }, 2000);
  } catch {
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(document.querySelector('#source-code'));
    selection.removeAllRanges(); selection.addRange(range);
    status.textContent = 'Code selected. Press Ctrl+C (Windows) or Command+C (Mac) to copy.';
  }
});

// One image per link: replace its source with the local fallback on failure.
document.querySelectorAll('img[data-logo-src]').forEach(image => {
  const fallback = image.getAttribute('src');
  image.addEventListener('error', () => { image.src = fallback; }, {once: true});
  image.src = image.dataset.logoSrc;
});

const search = document.querySelector('#material-search');
if (search) {
  const entries = JSON.parse(document.querySelector('#search-data').textContent);
  const results = document.querySelector('#search-results');
  const regular = document.querySelector('#browse-content');
  const count = document.querySelector('#search-count');
  const kind = document.querySelector('#material-kind');
  const week = document.querySelector('#material-week');
  const clear = document.querySelector('#clear-search');
  const prefix = document.body.dataset.root;
  document.querySelector('.search-controls').hidden = false;
  function restoreSearch() {
    const params = new URLSearchParams(window.location.search);
    search.value = params.get('q') || '';
    const savedKind = params.get('type') || '';
    kind.value = Array.from(kind.options).some(option => option.value === savedKind) ? savedKind : '';
    const savedWeek = params.get('week') || '';
    week.value = Array.from(week.options).some(option => option.value === savedWeek) ? savedWeek : '';
    updateSearch();
  }
  function updateSearch(save = false) {
    const query = search.value.trim().toLocaleLowerCase();
    const filtering = Boolean(query || kind.value || week.value);
    regular.hidden = filtering;
    results.hidden = !filtering;
    clear.hidden = !filtering;
    results.replaceChildren();
    count.textContent = '';
    if (save) {
      const url = new URL(window.location.href);
      for (const [key, value] of [['q', search.value.trim()], ['type', kind.value], ['week', week.value]]) {
        if (value) url.searchParams.set(key, value);
        else url.searchParams.delete(key);
      }
      // Keep a shareable URL and restore it when returning from an example.
      window.history.replaceState(null, '', url);
    }
    if (!filtering) return;
    const words = query.split(/\s+/).filter(Boolean);
    const matches = entries.filter(item => {
      const section = item.assignment != null ? 'assignments' : item.week === null ? 'resources' : String(item.week);
      return (!kind.value || item.kind === kind.value) && (!week.value || section === week.value) && words.every(word => item.search.includes(word));
    });
    count.textContent = `${matches.length} ${matches.length === 1 ? 'material' : 'materials'} found`;
    if (!matches.length) {
      const empty = document.createElement('p'); empty.className = 'empty';
      empty.textContent = 'No matches yet. Try a week number, a filename, a topic such as loops or strings, or choose All file types.';
      results.append(empty); return;
    }
    const list = document.createElement('div'); list.className = 'list';
    for (const item of matches) {
      const link = document.createElement('a'); link.className = 'file-row'; link.href = prefix + item.url;
      const kind = document.createElement('span'); kind.className = 'file-kind'; kind.textContent = item.kind;
      const info = document.createElement('div');
      const title = document.createElement('strong'); title.textContent = item.title;
      const path = document.createElement('small'); path.textContent = item.path;
      info.append(title, path);
      if (words.length && item.excerpt) {
        const content = item.excerpt.replace(/\s+/g, ' ');
        const startMatch = words.map(word => content.toLowerCase().indexOf(word)).filter(index => index >= 0).sort((a, b) => a - b)[0];
        if (startMatch !== undefined) {
          const start = Math.max(0, startMatch - 50);
          const snippet = (start ? '…' : '') + content.slice(start, start + 190) + (start + 190 < content.length ? '…' : '');
          const excerpt = document.createElement('small'); excerpt.className = 'search-excerpt';
          // Build text nodes and marks; course text is never treated as HTML.
          let offset = 0;
          while (offset < snippet.length) {
            const lower = snippet.toLowerCase();
            const next = words.map(word => ({word, at: lower.indexOf(word, offset)})).filter(match => match.at >= 0).sort((a, b) => a.at - b.at)[0];
            if (!next) { excerpt.append(document.createTextNode(snippet.slice(offset))); break; }
            excerpt.append(document.createTextNode(snippet.slice(offset, next.at)));
            const mark = document.createElement('mark'); mark.textContent = snippet.slice(next.at, next.at + next.word.length); excerpt.append(mark);
            offset = next.at + next.word.length;
          }
          info.append(excerpt);
        }
      }
      link.append(kind, info); list.append(link);
    }
    results.append(list);
  }
  search.addEventListener('input', () => updateSearch(true));
  kind.addEventListener('change', () => updateSearch(true));
  week.addEventListener('change', () => updateSearch(true));
  clear.addEventListener('click', () => {
    search.value = ''; kind.value = ''; week.value = '';
    updateSearch(true);
    search.focus();
  });
  window.addEventListener('popstate', restoreSearch);
  window.addEventListener('pageshow', restoreSearch);
  restoreSearch();
}

// Optional browser-local preferences and progress. Browsing works when storage is blocked.
const courseBase = new URL(document.body.dataset.root, location.href);
const progressKey = `cosc-progress:${courseBase.pathname}`;
const readingKey = `cosc-reading:${courseBase.pathname}`;
function readSaved(key) {
  try {
    const value = JSON.parse(localStorage.getItem(key));
    return value && typeof value === 'object' && !Array.isArray(value) ? value : {};
  } catch { return {}; }
}
function writeSaved(key, value) {
  try { localStorage.setItem(key, JSON.stringify(value)); return true; } catch { return false; }
}
const reading = document.querySelector('.reading-controls');
if (reading) {
  reading.hidden = false;
  const size = document.querySelector('#code-size');
  const wrap = document.querySelector('#code-wrap');
  const preferences = readSaved(readingKey);
  size.value = ['14', '16', '18'].includes(preferences.size) ? preferences.size : '14';
  wrap.checked = preferences.wrap === true;
  function applyReading() {
    document.documentElement.style.setProperty('--code-size', size.value + 'px');
    document.body.classList.toggle('wrap-code', wrap.checked);
    writeSaved(readingKey, {size: size.value, wrap: wrap.checked});
  }
  size.addEventListener('change', applyReading);
  wrap.addEventListener('change', applyReading);
  applyReading();
}
const progress = document.querySelector('.practice-progress');
if (progress) {
  progress.hidden = false;
  const checkbox = document.querySelector('#lesson-complete');
  const status = document.querySelector('#progress-save');
  const saved = readSaved(progressKey);
  checkbox.checked = saved.completed?.[progress.dataset.path] === true;
  function saveProgress() {
    const state = readSaved(progressKey);
    const completed = state.completed && typeof state.completed === 'object' && !Array.isArray(state.completed) ? state.completed : {};
    completed[progress.dataset.path] = checkbox.checked;
    const ok = writeSaved(progressKey, {last: progress.dataset.path, completed});
    status.textContent = ok ? 'Saved in this browser only.' : 'Progress could not be saved in this browser.';
  }
  checkbox.addEventListener('change', saveProgress);
  saveProgress();
}
const resume = document.querySelector('#resume-practice');
if (resume) {
  const entries = JSON.parse(document.querySelector('#search-data').textContent).filter(item => item.kind === 'PY');
  function showProgress() {
    const saved = readSaved(progressKey);
    const last = entries.find(item => item.path === saved.last);
    resume.replaceChildren();
    resume.hidden = !last;
    if (!last) return;
    const link = document.createElement('a'); link.className = 'button';
    link.href = new URL(last.url, courseBase).href; link.textContent = `Resume: ${last.title}`;
    const count = entries.filter(item => saved.completed?.[item.path] === true).length;
    const note = document.createElement('p'); note.textContent = `${count} of ${entries.length} examples marked as practised on this browser.`;
    resume.append(link, note);
  }
  window.addEventListener('pageshow', showProgress);
  window.addEventListener('storage', showProgress);
  showProgress();
}
