# COSC1100-05 demonstration code

Professor-led Python demonstrations for COSC1100-05. Weekly folders contain five core numbered scripts with pseudocode, desk checks, and classroom variations; selected weeks also include an optional sixth demo.

Use Python 3 and run a file from the repository root:

```bash
python3 week-3-demos/01_explore_data_types.py
```

On Windows, `py` may be used instead of `python3`. No pip dependencies are required. Weeks 11 and 12 require Tkinter and a graphical desktop; their guides include setup notes. Some console demos request keyboard input.

| Week | Topics |
| --- | --- |
| [2](week-2-demos/) | Existing algorithm and problem-solving demonstrations |
| [3](week-3-demos/README.md) | Working with data |
| [4](week-4-demos/README.md) | Selection and validation |
| [5](week-5-demos/README.md) | Iteration |
| [6](week-6-demos/README.md) | Iteration continued + midterm |
| [7](week-7-demos/README.md) | Mid-semester review |
| [8](week-8-demos/README.md) | Arrays |
| [9](week-9-demos/README.md) | Functions |
| [10](week-10-demos/README.md) | Arrays and functions continued |
| [11](week-11-demos/README.md) | User interfaces |
| [12](week-12-demos/README.md) | User interfaces continued |
| [13](week-13-demos/README.md) | Testing programs and user interfaces |
| [14](week-14-demos/README.md) | Review and final exam |

The requested arrays topics use Python lists. The “testing user” topic is interpreted as testing programs and user interfaces, including a live user-testing exercise. Midterm and final weeks contain practice and review examples rather than actual exams. Pricing, score bands, and other example rules are illustrative, not course policies.

Existing assignment files are separate from the weekly demonstration sequence.

## Instructor utilities and extensions

There are 68 demos across weeks 3–14, plus the five existing week 2 demos. Optional sixth demos cover decimal precision, short-circuit evaluation, running extremes, slicing/sorting, imports, selection sort, GUI timers, and testing the actual tracker rules. Use the first five as the core sequence; choose extensions to suit class time.

The [classroom utilities guide](utilities/README.md) explains the demo launcher, saved console checks, GUI setup probe, and printable trace-table and user-testing worksheets.

```bash
python3 utilities/demo_tools.py list --week 9
python3 utilities/demo_tools.py run 9 6
python3 utilities/demo_tools.py check
```

Most demos are standalone. The module-import demo uses `week-9-demos/study_helpers.py`; the week 12 score tracker uses `score_utils.py` in its own folder; week 13 demo 6 tests that same helper module. Keep those companion files when copying the examples.
