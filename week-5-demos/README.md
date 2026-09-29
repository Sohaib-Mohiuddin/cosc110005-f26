# Week 5: Iteration

Count-controlled and condition-controlled loops, accumulators, sentinels, and menus.

Five standalone Python demos for the professor to present in numerical order. Each file includes a problem, inputs and outputs, pseudocode, a desk check, and a try-it/discussion prompt.

## Run

From the repository root, using Python 3:

```bash
python3 week-5-demos/01_count_with_range.py
```

Replace the filename to run another demo. On Windows, `py` can be used in place of `python3`. No pip packages are required.

## Teaching sequence

| Demo | Focus |
| --- | --- |
| [01_count_with_range.py](01_count_with_range.py) | Repeat a known number of times |
| [02_trace_a_while_loop.py](02_trace_a_while_loop.py) | Track progress toward a loop condition |
| [03_accumulate_study_minutes.py](03_accumulate_study_minutes.py) | Accumulate values entered in a loop |
| [04_use_a_sentinel.py](04_use_a_sentinel.py) | Stop input with a sentinel value |
| [05_repeat_a_menu.py](05_repeat_a_menu.py) | Keep a menu running until exit |

## Classroom flow

1. Read the problem and ask students to identify inputs, processing, and outputs.
2. Trace the pseudocode and predict the desk-check result before running.
3. Run the demo, then change one input or requirement at a time.
4. Use the try-it and discussion prompts to check understanding.

Hardcoded inputs are near the top of early demos or in the guarded demonstration block in later demos. Interactive scripts prompt in the terminal. Deliberate bugs are clearly labelled; restore any classroom edits before proceeding.

Demo 3 assumes valid, nonnegative numeric input to keep attention on accumulation. Demos 4 and 5 handle invalid entries; week 6 adds a general retry pattern.
