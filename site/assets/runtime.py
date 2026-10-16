"""Browser execution driver. Only invoked after a student chooses a run action."""
import ast
import json
import linecache
import math
import os
import sys
import traceback
import types

_payload = json.loads(_runner_payload)
_filename = '/course/' + _payload['path']
_result = {'path': _payload['path'], 'trace': [], 'checks': [], 'sources': {}, 'traceLimited': False}
_namespace = {}


def _describe(value):
    if type(value) in (str, int, float, bool, type(None), list, tuple, dict, set):
        return repr(value)[:240]
    return '<' + type(value).__name__ + '>'


class _TraceLimit(Exception):
    pass


def _record(frame, event, arg):
    if not frame.f_code.co_filename.startswith('/course/'):
        return None
    if event in ('line', 'return'):
        if len(_result['trace']) >= 300:
            _result['traceLimited'] = True
            raise _TraceLimit('Trace stopped after 300 steps. Use a smaller input or Run without tracing.')
        path = frame.f_code.co_filename[len('/course/'):]
        values = {name: _describe(value) for name, value in list(frame.f_locals.items())[:40] if not name.startswith('__')}
        stack = []
        parent = frame
        while parent and len(stack) < 12:
            if parent.f_code.co_filename.startswith('/course/'):
                stack.append(parent.f_code.co_name)
            parent = parent.f_back
        _result['trace'].append({'line': frame.f_lineno, 'event': event, 'path': path, 'function': frame.f_code.co_name, 'variables': values, 'stack': stack})
        if path not in _result['sources']:
            try:
                with open(frame.f_code.co_filename) as source:
                    _result['sources'][path] = source.read()[:50000]
            except OSError:
                _result['sources'][path] = ''
    return _record


try:
    os.makedirs(os.path.dirname(_filename), exist_ok=True)
    os.chdir(os.path.dirname(_filename))
    sys.path.insert(0, os.getcwd())
    sys.path.extend(_payload.get('directories', []))
    sys.argv = [_filename]
    linecache.clearcache()
    _tree = ast.parse(_payload['code'], filename=_filename)
    _remaining = dict(_payload.get('overrides', {}))
    for _node in _tree.body:
        if isinstance(_node, ast.Assign) and len(_node.targets) == 1 and isinstance(_node.targets[0], ast.Name):
            _name = _node.targets[0].id
            if _name in _remaining:
                _node.value = ast.copy_location(ast.parse(repr(_remaining.pop(_name)), mode='eval').body, _node.value)
    if _remaining:
        raise ValueError('Sample check needs these supplied variable assignments: ' + ', '.join(_remaining))
    _compiled = compile(ast.fix_missing_locations(_tree), _filename, 'exec')
    if not _payload.get('syntaxOnly'):
        _module = types.ModuleType('__main__')
        _module.__file__ = _filename
        _module.__package__ = None
        sys.modules['__main__'] = _module
        _namespace = _module.__dict__
        try:
            if _payload.get('trace'):
                sys.settrace(_record)
            exec(_compiled, _namespace)
        except SystemExit as _exit:
            if _exit.code not in (None, 0):
                raise
        finally:
            sys.settrace(None)
        for _check in _payload.get('assertions', [])[:40]:
            try:
                _actual = eval(compile(ast.parse(_check['expression'], mode='eval'), '<practice check>', 'eval'), _namespace)
                _expected = _check.get('expected')
                if 'tolerance' in _check:
                    _ok = type(_actual) in (int, float) and type(_expected) in (int, float) and math.isclose(_actual, _expected, rel_tol=0, abs_tol=abs(_check['tolerance']))
                else:
                    _ok = _actual == _expected
                _result['checks'].append({'expression': _check['expression'], 'ok': bool(_ok), 'actual': _describe(_actual), 'expected': _describe(_expected)})
            except BaseException as _error:
                _result['checks'].append({'expression': _check['expression'], 'ok': False, 'actual': type(_error).__name__ + ': ' + str(_error), 'expected': _describe(_check.get('expected'))})
except BaseException as _error:
    sys.settrace(None)
    _frames = traceback.extract_tb(_error.__traceback__)
    _course_frames = [frame for frame in _frames if frame.filename.startswith('/course/')]
    _line = getattr(_error, 'lineno', None) or (_course_frames[-1].lineno if _course_frames else None)
    _path = getattr(_error, 'filename', None) or (_course_frames[-1].filename if _course_frames else _filename)
    _result['error'] = {'type': type(_error).__name__, 'line': _line, 'path': _path, 'message': str(_error)}
    _result['errorText'] = 'Traceback (most recent call last):\n' + ''.join(traceback.format_list(_course_frames)) + ''.join(traceback.format_exception_only(type(_error), _error))

json.dumps(_result)
