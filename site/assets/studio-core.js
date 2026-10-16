/* Shared browser-local tools. No student work is sent to a course server. */
(() => {
  const base = new URL(document.body.dataset.root, location.href);
  const prefix = `cosc-hub:${base.pathname}:`;
  const memory = new Map();
  const C = window.Course = {base, prefix};
  C.el = (tag, attrs = {}, ...children) => {
    const node = document.createElement(tag);
    for (const [key, value] of Object.entries(attrs)) {
      if (key === 'text') node.textContent = value;
      else node.setAttribute(key, value);
    }
    node.append(...children);
    return node;
  };
  C.read = (name, fallback = null) => {
    if (memory.has(name)) return memory.get(name);
    try { return JSON.parse(localStorage.getItem(prefix + name) || 'null') ?? fallback; }
    catch { return memory.get(name) ?? fallback; }
  };
  window.addEventListener('storage', event => { if (event.key?.startsWith(prefix)) memory.delete(event.key.slice(prefix.length)); });
  C.write = (name, value) => {
    memory.set(name, value);
    try { localStorage.setItem(prefix + name, JSON.stringify(value)); window.dispatchEvent(new CustomEvent('course:state', {detail: name})); return true; }
    catch { window.dispatchEvent(new CustomEvent('course:state', {detail: name})); return false; }
  };
  C.allowedKey = key => key.startsWith(prefix) || key.startsWith(`cosc-practice:${base.pathname}:`) || [`cosc-progress:${base.pathname}`, `cosc-reading:${base.pathname}`].includes(key);
  C.exportState = () => {
    const entries = {};
    try { for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (C.allowedKey(key)) entries[key] = localStorage.getItem(key);
    }
    } catch {}
    for (const [name, value] of memory) entries[prefix + name] = JSON.stringify(value);
    return {format: 'cosc-study-backup', version: 1, course: base.pathname, exported: new Date().toISOString(), entries};
  };
  C.validateBackup = backup => {
    if (!backup || backup.format !== 'cosc-study-backup' || backup.version !== 1 || backup.course !== base.pathname || !backup.entries || typeof backup.entries !== 'object' || Array.isArray(backup.entries)) throw new Error('Choose a study backup exported from this course.');
    const entries = Object.entries(backup.entries);
    if (entries.length > 2000 || JSON.stringify(backup).length > 8000000) throw new Error('This backup is too large (8 MB maximum).');
    for (const [key, value] of entries) {
      if (!C.allowedKey(key) || typeof value !== 'string') throw new Error('Backup contains an unsupported storage key.');
      const parsed = JSON.parse(value);
      if (key === prefix + 'projects') {
        if (!Array.isArray(parsed) || parsed.length > 30 || parsed.some(project => !project || typeof project.id !== 'string' || !/^[\w-]{1,80}$/.test(project.id) || typeof project.name !== 'string' || project.name.length > 160 || !project.files || Array.isArray(project.files) || typeof project.files !== 'object' || !Object.keys(project.files).length || Object.keys(project.files).length > 100 || Object.entries(project.files).some(([path, text]) => !C.validPath(path) || typeof text !== 'string' || text.length > 2000000))) throw new Error('The backup contains an invalid project. No items were restored.');
      }
      if (key === prefix + 'materials' && (!parsed || typeof parsed !== 'object' || Array.isArray(parsed) || Object.values(parsed).some(note => !note || typeof note !== 'object' || (note.note !== undefined && (typeof note.note !== 'string' || note.note.length > 12000))))) throw new Error('The backup contains invalid study notes.');
    }
    return entries;
  };
  C.restoreState = backup => {
    const entries = C.validateBackup(backup);
    const previous = entries.map(([key]) => [key, localStorage.getItem(key)]);
    try { for (const [key, value] of entries) localStorage.setItem(key, value); }
    catch {
      for (const [key, value] of previous) { try { if (value === null) localStorage.removeItem(key); else localStorage.setItem(key, value); } catch {} }
      throw new Error('The browser could not store this backup. Free some browser storage and retry.');
    }
    for (const [key, value] of entries) if (key.startsWith(prefix)) memory.set(key.slice(prefix.length), JSON.parse(value));
    window.dispatchEvent(new CustomEvent('course:state'));
    return entries.length;
  };
  C.download = (name, data, type = 'application/octet-stream') => {
    const url = URL.createObjectURL(data instanceof Blob ? data : new Blob([data], {type}));
    const link = C.el('a', {href: url, download: name}); document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1500);
  };
  C.validPath = path => typeof path === 'string' && path.length <= 180 && !/[\x00-\x1f\x7f\\:*?"<>|]/.test(path) && !path.split('/').some(part => !part || part === '.' || part === '..' || part.startsWith('.'));
  const crcTable = Array.from({length: 256}, (_, n) => { for (let k = 0; k < 8; k++) n = n & 1 ? 0xedb88320 ^ (n >>> 1) : n >>> 1; return n >>> 0; });
  C.zip = files => {
    const encoder = new TextEncoder(); const local = [], central = []; let offset = 0;
    const header = (size, values) => { const bytes = new Uint8Array(size), view = new DataView(bytes.buffer); for (const [at, value, width] of values) width === 4 ? view.setUint32(at, value, true) : view.setUint16(at, value, true); return bytes; };
    for (const file of files) {
      if (!C.validPath(file.path)) throw new Error('Invalid project filename: ' + file.path);
      const name = encoder.encode(file.path), bytes = typeof file.content === 'string' ? encoder.encode(file.content) : new Uint8Array(file.bytes);
      let crc = 0xffffffff; for (const byte of bytes) crc = crcTable[(crc ^ byte) & 255] ^ (crc >>> 8); crc = (crc ^ 0xffffffff) >>> 0;
      const h = header(30, [[0,0x04034b50,4],[4,20,2],[6,0x800,2],[14,crc,4],[18,bytes.length,4],[22,bytes.length,4],[26,name.length,2]]);
      local.push(h,name,bytes);
      central.push(header(46, [[0,0x02014b50,4],[4,20,2],[6,20,2],[8,0x800,2],[16,crc,4],[20,bytes.length,4],[24,bytes.length,4],[28,name.length,2],[42,offset,4]]),name);
      offset += h.length + name.length + bytes.length;
    }
    const centralSize = central.reduce((sum, bytes) => sum + bytes.length, 0);
    return new Blob([...local,...central,header(22,[[0,0x06054b50,4],[8,files.length,2],[10,files.length,2],[12,centralSize,4],[16,offset,4]])],{type:'application/zip'});
  };
  C.compare = (actual, check = {}) => {
    const mode = check.mode || 'contains';
    let ok = false, reason = '';
    if (mode === 'contains') { const missing = (check.contains || [String(check.expected ?? '')]).filter(part => !actual.includes(part)); ok = missing.length === 0; reason = 'Missing output: ' + missing.join(', '); }
    else if (mode === 'exact') { ok = actual.replace(/\r\n/g,'\n').trimEnd() === String(check.expected ?? '').replace(/\r\n/g,'\n').trimEnd(); reason = 'Output differs from the expected text.'; }
    else if (mode === 'number') { const value = Number(actual.trim()), expected = Number(check.expected), tolerance = Math.abs(Number(check.tolerance) || 0); ok = actual.trim() !== '' && String(check.expected ?? '').trim() !== '' && Number.isFinite(value) && Number.isFinite(expected) && Number.isFinite(tolerance) && Math.abs(value - expected) <= tolerance; reason = 'Expected a single number within the chosen tolerance.'; }
    else if (mode === 'json') {
      const sorted = value => Array.isArray(value) ? value.map(sorted) : value && typeof value === 'object' ? Object.fromEntries(Object.keys(value).sort().map(key => [key, sorted(value[key])])) : value;
      try { ok = JSON.stringify(sorted(JSON.parse(actual))) === JSON.stringify(sorted(typeof check.expected === 'string' ? JSON.parse(check.expected) : check.expected)); } catch {}
      reason = 'Expected matching JSON values (object key order does not matter).';
    } else reason = 'Unknown comparison mode.';
    return {ok, reason: ok ? 'Matched expected result.' : reason, expected: check.expected ?? check.contains?.join('\n') ?? ''};
  };
  C.explain = error => {
    const rules = [
      ['IndentationError','Python uses indentation to group statements.','Align statements in the same block, and indent the body after a colon.','if ready:\n    print("Go")'],
      ['SyntaxError','Python could not understand this statement.','Check the highlighted line and the line above it for missing colons, quotes or brackets.','for item in items:\n    print(item)'],
      ['NameError','A name was used before Python knew its value.','Check spelling and capitalization, then find where that variable is assigned.','message = "Hello"\nprint(message)'],
      ['TypeError','An operation received an unsuitable type of value.','Inspect the values and their types. Convert input text before numeric arithmetic.','age = int(input("Age: "))\nprint(age + 1)'],
      ['ValueError','A value could not be used in the requested way.','For conversions, check what the input contains and handle invalid text.','try:\n    count = int(text)\nexcept ValueError:\n    print("Enter a whole number")'],
      ['ZeroDivisionError','The program tried to divide by zero.','Check the denominator before dividing; an empty collection may have a count of zero.','if count > 0:\n    average = total / count'],
      ['IndexError','A sequence position is outside its valid range.','Check the index and the sequence length; the final index is length minus one.','for item in values:\n    print(item)'],
      ['KeyError','A dictionary does not contain this key.','Check the key, or choose a default with get().','score = scores.get("Alex", 0)'],
      ['EOFError','The program requested another answer.','Add all answers to Program input, one per line, including any stop value.','name = input("Name: ")'],
      ['ModuleNotFoundError','Python could not find an imported module.','Add the companion .py file to your project, check the filename, or use desktop Python for unavailable packages.','from helper import calculate'],
      ['FileNotFoundError','The requested file was not found.','Upload the file and check its path relative to the program’s folder.','with open("data.csv") as data:\n    print(data.read())']
    ];
    const match = rules.find(rule => String(error).includes(rule[0]));
    return match ? {type:match[0],title:match[1],tip:match[2],example:match[3]} : {type:'Run help',title:'The run could not finish.',tip:'Read the final error message, check loop conditions and input, then try a smaller example.',example:''};
  };
  C.showError = (host, message, detail, editor) => {
    host.replaceChildren(); if (!message) {host.hidden = true;return;}
    host.hidden = false; const help = C.explain(message);
    host.append(C.el('h3',{text:help.type + ': ' + help.title}),C.el('p',{text:help.tip}));
    if (detail?.line && editor) {const jump=C.el('button',{class:'button small',type:'button',text:`Go to line ${detail.line}`});jump.addEventListener('click',()=>C.jump(editor,detail.line));host.append(jump);}
    if(help.example)host.append(C.el('pre',{text:help.example}));
  };
  C.jump = (textarea, line) => {
    const lines=textarea.value.split('\n');const start=lines.slice(0,line-1).reduce((n,s)=>n+s.length+1,0);textarea.focus();textarea.setSelectionRange(start,start+(lines[line-1]?.length||0));textarea.scrollTop=Math.max(0,(line-3)*parseFloat(getComputedStyle(textarea).lineHeight));textarea.dispatchEvent(new Event('scroll'));
  };
  const escape = text => text.replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  C.highlight = line => {
    const regex = /(#.*$|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\b(?:and|as|assert|async|await|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield)\b|\b\d+(?:\.\d+)?\b)/g;
    let html='', at=0; for (const match of line.matchAll(regex)) {html+=escape(line.slice(at,match.index));const token=match[0],kind=token.startsWith('#')?'comment':/^["']/.test(token)?'string':/^\d/.test(token)?'number':'keyword';html+=`<span class="tok-${kind}">${escape(token)}</span>`;at=match.index+token.length;}return html+escape(line.slice(at));
  };
  C.enhanceEditor = textarea => {
    if(textarea.dataset.enhanced)return;textarea.dataset.enhanced='true';
    const frame=C.el('div',{class:'editor-frame'}), preview=C.el('pre',{class:'editor-highlight','aria-hidden':'true'});textarea.before(frame);frame.append(preview,textarea);
    const render=()=>{preview.innerHTML=textarea.value.split('\n').map((line,index)=>`<span class="editor-line" data-line="${index+1}">${C.highlight(line)||' '}</span>`).join('');preview.scrollTop=textarea.scrollTop;preview.scrollLeft=textarea.scrollLeft;};
    textarea.addEventListener('input',render);textarea.addEventListener('scroll',()=>{preview.scrollTop=textarea.scrollTop;preview.scrollLeft=textarea.scrollLeft;});textarea.addEventListener('keydown',event=>{if(event.key==='Enter'&&!event.ctrlKey&&!event.metaKey){const before=textarea.value.slice(0,textarea.selectionStart).split('\n').pop();const indent=(before.match(/^\s*/)?.[0]||'')+(/:\s*$/.test(before)?'    ':'');event.preventDefault();textarea.setRangeText('\n'+indent,textarea.selectionStart,textarea.selectionEnd,'end');textarea.dispatchEvent(new Event('input',{bubbles:true}));}if((event.ctrlKey||event.metaKey)&&['[',']'].includes(event.key)){event.preventDefault();C.indent(textarea,event.key==='[');}});
    textarea.courseRender=render;render();
  };
  C.indent=(textarea,remove=false)=>{const start=textarea.value.lastIndexOf('\n',textarea.selectionStart-1)+1;const end=textarea.selectionEnd;const selection=textarea.value.slice(start,end);const changed=selection.split('\n').map(line=>remove?line.replace(/^ {1,4}/,''):'    '+line).join('\n');textarea.setRangeText(changed,start,end,'select');textarea.dispatchEvent(new Event('input',{bubbles:true}));};
})();
