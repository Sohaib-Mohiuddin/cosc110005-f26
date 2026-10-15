// Pinned runtime: updates are deliberate and verified by the browser smoke tests.
const runtimeURL = 'https://cdn.jsdelivr.net/pyodide/v314.0.7/full/pyodide.mjs';
const MAX_OUTPUT = 65536;

self.onmessage = async ({data}) => {
  let pending = '';
  let size = 0;
  let started = false;
  const flush = () => {
    if (pending) self.postMessage({type: 'output', text: pending});
    pending = '';
  };
  try {
    const {loadPyodide} = await import(runtimeURL);
    const py = await loadPyodide();
    const decoder = new TextDecoder();
    const write = bytes => {
      size += bytes.length;
      if (size > MAX_OUTPUT) {
        const message = 'Output limit reached (64 KB). Reduce printing and try again.';
        flush();
        // Notify the parent immediately, even if Python catches the write error.
        self.postMessage({type: 'error', text: message});
        throw new Error(message);
      }
      pending += decoder.decode(bytes, {stream: true});
      if (pending.length >= 2048 || pending.includes('\n')) flush();
      return bytes.length;
    };
    py.setStdout({write});
    py.setStderr({write});
    const input = data.stdin.replace(/\r\n?/g, '\n');
    const lines = input === '' ? [] : input.split('\n');
    if (input.endsWith('\n')) lines.pop();
    py.setStdin({stdin: () => lines.shift()});
    for (const file of data.files) {
      // Files come only from the build's released-material manifest.
      const path = '/course/' + file.path;
      py.FS.mkdirTree(path.substring(0, path.lastIndexOf('/')));
      py.FS.writeFile(path, new Uint8Array(file.bytes));
    }
    const selectedPath = '/course/' + data.path;
    py.FS.mkdirTree(selectedPath.substring(0, selectedPath.lastIndexOf('/')));
    py.FS.writeFile(selectedPath, data.code);
    py.globals.set('_runner_payload', JSON.stringify({code: data.code, path: data.path, overrides: data.overrides || {}, directories: [...new Set(data.files.map(file => '/course/' + file.path.substring(0, file.path.lastIndexOf('/') + 1)))]}));
    started = true;
    self.postMessage({type: 'running'});
    await py.runPythonAsync(`
import ast, json, os, sys, types
_payload = json.loads(_runner_payload)
_filename = '/course/' + _payload['path']
os.makedirs(os.path.dirname(_filename), exist_ok=True)
os.chdir(os.path.dirname(_filename))
sys.path.insert(0, os.getcwd())
sys.path.extend(_payload['directories'])
sys.argv = [_filename]
_tree = ast.parse(_payload['code'], filename=_filename)
_remaining = dict(_payload['overrides'])
for _node in _tree.body:
    if isinstance(_node, ast.Assign) and len(_node.targets) == 1 and isinstance(_node.targets[0], ast.Name):
        _name = _node.targets[0].id
        if _name in _remaining:
            _node.value = ast.copy_location(ast.parse(repr(_remaining.pop(_name)), mode='eval').body, _node.value)
if _remaining:
    raise ValueError('Sample check needs these supplied variable assignments: ' + ', '.join(_remaining))
_module = types.ModuleType('__main__')
_module.__file__ = _filename
_module.__package__ = None
sys.modules['__main__'] = _module
_namespace = _module.__dict__
try:
    exec(compile(ast.fix_missing_locations(_tree), _filename, 'exec'), _namespace)
except SystemExit as _exit:
    if _exit.code not in (None, 0):
        raise
`);
    flush();
    self.postMessage({type: 'done'});
  } catch (error) {
    flush();
    const hint = started ? '' : 'Python could not load. Check your connection and retry, or download the lesson for desktop Python.\n';
    self.postMessage({type: 'error', text: hint + String(error.message || error)});
  }
};
