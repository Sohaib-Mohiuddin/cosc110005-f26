const menu = document.querySelector('.menu-toggle');
const sidebar = document.querySelector('.sidebar');
function closeMenu() { sidebar.classList.remove('open'); menu?.setAttribute('aria-expanded', 'false'); }
menu?.addEventListener('click', () => {
  const open = sidebar.classList.toggle('open');
  menu.setAttribute('aria-expanded', String(open));
});
document.addEventListener('keydown', event => { if (event.key === 'Escape' && sidebar.classList.contains('open')) { closeMenu(); menu?.focus(); } });
document.addEventListener('click', event => { if (!sidebar.contains(event.target) && !menu?.contains(event.target)) closeMenu(); });

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

const search = document.querySelector('#material-search');
if (search) {
  const entries = JSON.parse(document.querySelector('#search-data').textContent);
  const results = document.querySelector('#search-results');
  const regular = document.querySelector('#browse-content');
  const count = document.querySelector('#search-count');
  const prefix = document.body.dataset.root;
  function updateSearch() {
    const query = search.value.trim().toLocaleLowerCase();
    regular.hidden = Boolean(query);
    results.hidden = !query;
    results.replaceChildren();
    count.textContent = '';
    if (!query) return;
    const words = query.split(/\s+/);
    const matches = entries.filter(item => words.every(word => item.search.includes(word)));
    count.textContent = `${matches.length} ${matches.length === 1 ? 'material' : 'materials'} found`;
    if (!matches.length) {
      const empty = document.createElement('p'); empty.className = 'empty';
      empty.textContent = 'No matches yet. Try a week number, a filename, or a topic such as loops or strings.';
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
  search.addEventListener('input', updateSearch);
  updateSearch();
}
