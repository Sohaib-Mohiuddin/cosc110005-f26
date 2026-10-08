const menu = document.querySelector('.menu-toggle');
const sidebar = document.querySelector('.sidebar');
function closeMenu() { sidebar.classList.remove('open'); menu?.setAttribute('aria-expanded', 'false'); }
menu?.addEventListener('click', () => {
  const open = sidebar.classList.toggle('open');
  menu.setAttribute('aria-expanded', String(open));
});
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

// Keep the book icon until a logo loads, including cached images and failures.
document.querySelectorAll('.link-logo img').forEach(image => {
  const updateLogo = () => {
    image.parentElement.classList.toggle('is-loaded', image.complete && image.naturalWidth > 0);
  };
  image.addEventListener('load', updateLogo);
  image.addEventListener('error', updateLogo);
  updateLogo();
});

const search = document.querySelector('#material-search');
if (search) {
  const entries = JSON.parse(document.querySelector('#search-data').textContent);
  const results = document.querySelector('#search-results');
  const regular = document.querySelector('#browse-content');
  const count = document.querySelector('#search-count');
  const kind = document.querySelector('#material-kind');
  const clear = document.querySelector('#clear-search');
  const prefix = document.body.dataset.root;
  document.querySelector('.search-controls').hidden = false;
  function restoreSearch() {
    const params = new URLSearchParams(window.location.search);
    search.value = params.get('q') || '';
    const savedKind = params.get('type') || '';
    kind.value = Array.from(kind.options).some(option => option.value === savedKind) ? savedKind : '';
    updateSearch();
  }
  function updateSearch(save = false) {
    const query = search.value.trim().toLocaleLowerCase();
    const filtering = Boolean(query || kind.value);
    regular.hidden = filtering;
    results.hidden = !filtering;
    clear.hidden = !filtering;
    results.replaceChildren();
    count.textContent = '';
    if (save) {
      const url = new URL(window.location.href);
      for (const [key, value] of [['q', search.value.trim()], ['type', kind.value]]) {
        if (value) url.searchParams.set(key, value);
        else url.searchParams.delete(key);
      }
      // Keep a shareable URL and restore it when returning from an example.
      window.history.replaceState(null, '', url);
    }
    if (!filtering) return;
    const words = query.split(/\s+/).filter(Boolean);
    const matches = entries.filter(item => (!kind.value || item.kind === kind.value) && words.every(word => item.search.includes(word)));
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
      info.append(title, path); link.append(kind, info); list.append(link);
    }
    results.append(list);
  }
  search.addEventListener('input', () => updateSearch(true));
  kind.addEventListener('change', () => updateSearch(true));
  clear.addEventListener('click', () => {
    search.value = ''; kind.value = '';
    updateSearch(true);
    search.focus();
  });
  window.addEventListener('popstate', restoreSearch);
  window.addEventListener('pageshow', restoreSearch);
  restoreSearch();
}
