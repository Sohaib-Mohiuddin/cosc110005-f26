# Week 11: User interfaces

Tkinter windows, widgets, callbacks, entry fields, choices, and forms.

Five standalone Python demos for the professor to present in numerical order. Each file includes a problem, inputs and outputs, pseudocode, a desk check, and a try-it/discussion prompt.

## Run

From the repository root, using Python 3:

```bash
python3 week-11-demos/01_open_a_window.py
```

Replace the filename to run another demo. On Windows, `py` can be used in place of `python3`. No pip packages are required.

## Teaching sequence

| Demo | Focus |
| --- | --- |
| [01_open_a_window.py](01_open_a_window.py) | Introduce widgets and the event loop |
| [02_read_a_name.py](02_read_a_name.py) | Read entry text and display feedback |
| [03_convert_temperature.py](03_convert_temperature.py) | Keep calculations separate from GUI callbacks |
| [04_choose_an_activity.py](04_choose_an_activity.py) | Use radio buttons for one choice |
| [05_build_a_registration_form.py](05_build_a_registration_form.py) | Combine labelled fields in a form |

## Classroom flow

1. Read the problem and ask students to identify inputs, processing, and outputs.
2. Trace the pseudocode and predict the desk-check result before running.
3. Run the demo, then change one input or requirement at a time.
4. Use the try-it and discussion prompts to check understanding.

Hardcoded inputs are near the top of early demos or in the guarded demonstration block in later demos. Interactive scripts prompt in the terminal. Deliberate bugs are clearly labelled; restore any classroom edits before proceeding.

## GUI setup and verification

These demos require Tkinter and a graphical desktop. Check the local Python installation with `python3 -m tkinter`; it should open a test window. If Tkinter is missing, install the Tcl/Tk support appropriate to your Python installation (commonly `python3-tk` on Debian/Ubuntu). A headless terminal without a display cannot show these windows.

Run one demo at a time and close its window to finish. All data stays in memory. Use the desk check in each file as the manual verification script, then try invalid input, keyboard navigation, repeated actions, and resizing where relevant. Nothing is sent or saved by these demos.
