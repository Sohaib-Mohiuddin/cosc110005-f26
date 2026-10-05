# Week 6: Iteration continued + midterm

Retry loops, nested loops, break/continue, tracing, and cumulative midterm practice.

Five core Python demos plus an optional extension for the professor to present in numerical order. Each file includes a problem, inputs and outputs, pseudocode, a desk check, and a try-it/discussion prompt.

## Run

From the repository root, using Python 3:

```bash
python3 week-6-demos/01_retry_until_valid.py
```

Replace the filename to run another demo. On Windows, `py` can be used in place of `python3`. No pip packages are required.

## Teaching sequence

| Demo | Focus |
| --- | --- |
| [01_retry_until_valid.py](01_retry_until_valid.py) | Repeat validation until input is acceptable |
| [02_nest_loops.py](02_nest_loops.py) | Trace nested loops with a seating chart |
| [03_use_break_and_continue.py](03_use_break_and_continue.py) | Distinguish skipping from stopping |
| [04_find_an_off_by_one_error.py](04_find_an_off_by_one_error.py) | Use a trace to diagnose loop bounds |
| [05_midterm_practice.py](05_midterm_practice.py) | Combine data, decisions, and iteration |
| [06_track_running_extremes.py](06_track_running_extremes.py) | Optional extension: Find minimum and maximum values as input arrives |

## Classroom flow

1. Read the problem and ask students to identify inputs, processing, and outputs.
2. Trace the pseudocode and predict the desk-check result before running.
3. Run the demo, then change one input or requirement at a time.
4. Use the try-it and discussion prompts to check understanding.

Hardcoded inputs are near the top of early demos or in the guarded demonstration block in later demos. Interactive scripts prompt in the terminal. Deliberate bugs are clearly labelled; restore any classroom edits before proceeding.

These are review and practice materials, not an actual exam, an exam answer key, or an official grading policy. Hide the worked code initially and ask students to sketch their own algorithm and test cases.
