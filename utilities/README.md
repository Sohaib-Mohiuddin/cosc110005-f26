# Classroom utilities

These optional instructor tools use only the Python standard library. They do not need to be taught before the demos. Paths are resolved from the utility file, so the tools also work when launched from a different working directory. Use `py` instead of `python3` on Windows if appropriate.

From the repository root:

```bash
# See the available demos and which ones open a GUI.
python3 utilities/demo_tools.py list
python3 utilities/demo_tools.py list --week 8

# Launch week 9, demo 6, with normal terminal input/output.
python3 utilities/demo_tools.py run 9 6

# Check every week's syntax and run saved console examples.
python3 utilities/demo_tools.py check
python3 utilities/demo_tools.py check --week 13

# Before teaching the interface weeks, probe Tkinter and the display.
python3 utilities/demo_tools.py doctor
```

`check` compiles every Python file in the selected week folders without writing bytecode, then runs the console scenarios in [demo_cases.json](demo_cases.json). A nonzero exit, missing expected output, syntax error, or five-second timeout causes a failure. It includes ordinary examples and selected invalid-input/boundary cases. These are smoke checks, not exhaustive proofs of correctness. Only run the checker on demo code you intend to execute; it runs the scripts normally.

GUI demos receive syntax checks but are not opened by `check`. `doctor` verifies only that Tkinter can create a window. Follow the GUI demos' desk checks to verify visual layout, callbacks, keyboard controls, timers, and state changes. Week 13 demo 6 separately tests the score tracker's actual parsing and average functions without needing Tkinter.

When adding a numbered demo, add its repository-relative path to `demo_cases.json`. Console entries need `"mode": "console"` and at least one case with `"stdin"` and a nonempty `"contains"` list. Include a final newline in keyboard input. GUI entries need only `"mode": "gui"`. Derive expected results independently from the problem statement.

The launcher discovers `NN_name.py` files, so companion modules are not shown as demos. Keep `week-9-demos/study_helpers.py` alongside its importing demo and `week-12-demos/score_utils.py` alongside the score tracker. Week 13 demo 6 also needs the neighbouring week 12 folder.

Reusable classroom handouts:

- [Trace table](trace_table.md): predict variable changes before running code.
- [User-testing worksheet](user_testing_worksheet.md): record tasks, observations, and defects.
