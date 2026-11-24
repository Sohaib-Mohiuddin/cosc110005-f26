# Week 11: User interfaces

Tkinter windows, widgets, callbacks, entry fields, choices, and forms.

Six standalone Python demos for the professor to present in numerical order. Each file includes a problem, inputs and outputs, pseudocode, a desk check, and a try-it/discussion prompt.

## Run

From the repository root, using Python 3:

```bash
python3 week-11-demos/01_open_a_window.py
```

Replace the filename to run another demo. On Windows, use `py` in place of `python3`. All six demos run with standard Tkinter. Demo 6 also supports the optional `ttkbootstrap` theme and widget styles.

## Teaching sequence

| Demo | Focus |
| --- | --- |
| [01_open_a_window.py](01_open_a_window.py) | Introduce widgets and the event loop |
| [02_read_a_name.py](02_read_a_name.py) | Read entry text and display feedback |
| [03_convert_temperature.py](03_convert_temperature.py) | Keep calculations separate from GUI callbacks |
| [04_choose_an_activity.py](04_choose_an_activity.py) | Use radio buttons for one choice |
| [05_build_a_registration_form.py](05_build_a_registration_form.py) | Combine labelled fields in a form |
| [06_build_a_study_planner.py](06_build_a_study_planner.py) | Connect validation, list processing, search, sorting, and progress to an interactive dashboard |

## Demo 6 — Study Session Planner

Run it from the repository root using desktop Python:

```bash
python3 week-11-demos/06_build_a_study_planner.py
```

For the themed version, run `python3 -m pip install ttkbootstrap` in the same Python environment, then launch the script again. On Windows, use `py -m pip install ttkbootstrap`. See the [ttkbootstrap installation guide](https://www.ttkbootstrap.org/en/latest/user-guide/getting-started/installation.html) for virtual environment and platform instructions.

| Week | What to trace in the planner |
| --- | --- |
| 2 | Identify inputs, processing, and outputs in the pseudocode. Trace one click from the form to the table. |
| 3 | Convert widget text to an integer, trim titles, store a Boolean, and format the percentage. |
| 4 | Check input bounds and compare text with Boolean conditions. Show feedback on conversion errors. |
| 5 | Accumulate planned and completed minutes. Compare repeated button events with a console menu loop. |
| 6 | Trace the nested selection sort and reset the per-topic accumulator. Use `continue` to skip unmatched rows. |
| 7 | Combine validation, decisions, and totals in one workflow. Predict the outcome before trying invalid entries. |
| 8 | Add, index, update, remove, and traverse rows in a two-dimensional list. |
| 9 | Follow parameters, a default argument, returned values, and local variables. Compare calculation functions with callbacks. |
| 10 | Filter into a separate index list and sort that view while retaining the plan's original order. |
| 11 | Connect a text entry, read-only topic picker, spinbox, checkbox, scrollable table, and progress bar to callbacks. |

For later review, use this project to preview Week 12's interface state and resizing, Week 13's boundary and workflow testing, and Week 14's separation of calculation from presentation. The validation, search, and summary functions can be called without opening a window.

Try entering minutes `0`, `1`, `180`, and `181`. Then add two sessions, filter to the second, and mark it done. Clear the filter and check which row changed. Toggle **Shortest first** and repeat the check after removing a row. Use Tab and Enter to submit from either text field, and resize the window to see how the table grows.

Hover over a control or pause on it while tabbing to read its tooltip. Hover over the progress bar to see what counts toward the goal. Press Escape to dismiss a tooltip.

## Classroom flow

1. Read the problem and ask students to identify inputs, processing, and outputs.
2. Trace the pseudocode and predict the desk-check result before running.
3. Run the demo, then change one input or requirement at a time.
4. Use the try-it and discussion prompts to check understanding.

Hardcoded inputs are near the top of early demos or in the guarded demonstration block in later demos. Interactive scripts prompt in the terminal. Deliberate bugs are clearly labelled; restore any classroom edits before proceeding.

## GUI setup and verification

These demos require Tkinter and a graphical desktop. Check the local Python installation with `python3 -m tkinter`; it should open a test window. If Tkinter is missing, install the Tcl/Tk support appropriate to your Python installation (commonly `python3-tk` on Debian/Ubuntu). A headless terminal without a display cannot show these windows.

Run one demo at a time and close its window to finish. All data stays in memory. Use the desk check in each file as the manual verification script, then try invalid input, keyboard navigation, repeated actions, and resizing where relevant. Nothing is sent or saved by these demos.
