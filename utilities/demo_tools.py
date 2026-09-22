"""List, launch, and check course demos using only Python's standard library."""

import argparse
import ast
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CASE_FILE = Path(__file__).with_name("demo_cases.json")


def discover(week=None):
    """Find numbered demos only; companion modules are not launch targets."""
    weeks = [week] if week is not None else range(2, 15)
    return [path for number in weeks
            for path in sorted((ROOT / f"week-{number}-demos").glob("[0-9][0-9]_*.py"))]


def load_cases(paths):
    """Require an explicit GUI marker or at least one console check per demo."""
    cases = json.loads(CASE_FILE.read_text(encoding="utf-8"))
    if not isinstance(cases, dict):
        raise ValueError(f"{CASE_FILE.name} must contain an object keyed by demo path")
    for path in paths:
        key = path.relative_to(ROOT).as_posix()
        entry = cases.get(key)
        if not isinstance(entry, dict) or entry.get("mode") not in ("console", "gui"):
            raise ValueError(f"Add a console or gui entry to {CASE_FILE.name}: {key}")
        if entry["mode"] == "console":
            scenarios = entry.get("cases")
            if not isinstance(scenarios, list) or not scenarios:
                raise ValueError(f"No console scenarios for {key}")
            for scenario in scenarios:
                if not isinstance(scenario, dict):
                    raise ValueError(f"Invalid scenario for {key}")
                expected = scenario.get("contains")
                if (not isinstance(scenario.get("stdin"), str)
                        or not isinstance(expected, list) or not expected
                        or not all(isinstance(text, str) and text for text in expected)):
                    raise ValueError(f"Each scenario needs stdin text and nonempty contains strings: {key}")
    return cases


def list_demos(paths, cases):
    for path in paths:
        key = path.relative_to(ROOT).as_posix()
        docstring = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or path.stem
        print(f"{key} [{cases[key]['mode']}]\n  {docstring.splitlines()[0]}")
    print(f"{len(paths)} demos")
    return 0


def check_demos(paths, cases):
    """Check syntax, then execute console scenarios with bounded input and time."""
    failures = 0
    syntax_failures = set()
    # Include companion modules as well as numbered demos in the syntax check.
    source_files = sorted({source for path in paths for source in path.parent.glob("*.py")})
    for source in source_files:
        try:
            compile(source.read_text(encoding="utf-8"), str(source), "exec")
        except SyntaxError as error:
            failures += 1
            syntax_failures.add(source)
            print(f"FAIL syntax: {source.relative_to(ROOT)}: {error}")
    print(f"Syntax: {len(source_files) - len(syntax_failures)}/{len(source_files)} files passed")

    scenarios_run = 0
    scenarios_passed = 0
    skipped = 0
    for path in paths:
        key = path.relative_to(ROOT).as_posix()
        entry = cases[key]
        if entry["mode"] == "gui":
            skipped += 1
            continue
        if path in syntax_failures:
            continue
        for number, scenario in enumerate(entry["cases"], 1):
            scenarios_run += 1
            try:
                # An argument list preserves paths containing spaces and avoids a shell.
                result = subprocess.run(
                    [sys.executable, "-B", str(path)], cwd=path.parent,
                    input=scenario["stdin"], text=True, capture_output=True, timeout=5,
                )
            except subprocess.TimeoutExpired:
                failures += 1
                print(f"FAIL {key} case {number}: exceeded 5 seconds")
                continue
            output = result.stdout + result.stderr
            missing = [text for text in scenario["contains"] if text not in output]
            if result.returncode != 0 or missing:
                failures += 1
                print(f"FAIL {key} case {number}: exit={result.returncode}; missing={missing}")
                print(output[-2000:])
            else:
                scenarios_passed += 1
    print(f"Console scenarios: {scenarios_passed}/{scenarios_run} passed")
    print(f"GUI demos: {skipped} skipped (syntax checked; use the weekly manual checks)")
    print(f"Failures: {failures}")
    return 1 if failures else 0


def check_gui_setup():
    """Probe the local Tk installation/display; this is not a visual demo test."""
    print(f"Python: {sys.version.split()[0]} ({sys.executable})")
    try:
        import tkinter as tk
    except ImportError:
        print("Tkinter is unavailable. See week-11-demos/README.md for setup notes.")
        return 1
    window = None
    try:
        window = tk.Tk()
        window.withdraw()
        window.update_idletasks()
        print(f"Tk {tk.TkVersion}: a window can be created on this display.")
    except tk.TclError as error:
        print(f"Tkinter is installed but could not create a window: {error}")
        return 1
    finally:
        if window is not None:
            window.destroy()
    print("Next, run a GUI demo and follow its desk check.")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list", help="list demos, optionally for one week")
    listing.add_argument("--week", type=int, choices=range(2, 15))
    running = commands.add_parser("run", help="run one demo with live keyboard input")
    running.add_argument("week", type=int, choices=range(2, 15))
    running.add_argument("demo", type=int, help="number from the filename, such as 1 or 6")
    checking = commands.add_parser("check", help="check syntax and run saved console scenarios")
    checking.add_argument("--week", type=int, choices=range(2, 15))
    commands.add_parser("doctor", help="check whether this machine can create Tkinter windows")
    args = parser.parse_args()
    if args.command == "doctor":
        return check_gui_setup()
    paths = discover(args.week)
    if args.command == "run":
        selected = [path for path in paths if int(path.name[:2]) == args.demo]
        if len(selected) != 1:
            parser.error(f"No unique demo {args.demo} in week {args.week}; use list --week {args.week}")
        # Inherit terminal input/output for interactive and GUI demonstrations.
        return subprocess.run([sys.executable, "-B", str(selected[0])], cwd=selected[0].parent).returncode
    try:
        cases = load_cases(paths)
        if args.command == "list":
            return list_demos(paths, cases)
        return check_demos(paths, cases)
    except (OSError, ValueError, SyntaxError) as error:
        parser.exit(1, f"Cannot complete {args.command}: {error}\n")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
