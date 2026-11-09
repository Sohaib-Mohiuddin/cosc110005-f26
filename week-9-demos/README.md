# Week 9: Functions

Definitions, calls, parameters, return values, local scope, and decomposition.

Five core Python demos plus an optional extension for the professor to present in numerical order. Each file includes a problem, inputs and outputs, pseudocode, a desk check, and a try-it/discussion prompt.

## Run

From the repository root, using Python 3:

```bash
python3 week-9-demos/01_define_and_call_functions.py
```

Replace the filename to run another demo. On Windows, `py` can be used in place of `python3`. No pip packages are required.

## Teaching sequence

| Demo | Focus |
| --- | --- |
| [01_define_and_call_functions.py](01_define_and_call_functions.py) | Define a function and call it more than once |
| [02_pass_arguments.py](02_pass_arguments.py) | Pass values into parameters |
| [03_return_a_result.py](03_return_a_result.py) | Return a value for the caller to use |
| [04_understand_local_scope.py](04_understand_local_scope.py) | Distinguish local values from caller values |
| [05_compose_small_functions.py](05_compose_small_functions.py) | Split a program into focused functions |
| [06_import_a_helper_module.py](06_import_a_helper_module.py) | Optional extension: Reuse functions from a neighbouring module |

## Classroom flow

1. Read the problem and ask students to identify inputs, processing, and outputs.
2. Trace the pseudocode and predict the desk-check result before running.
3. Run the demo, then change one input or requirement at a time.
4. Use the try-it and discussion prompts to check understanding.

Hardcoded inputs are near the top of early demos or in the guarded demonstration block in later demos. Interactive scripts prompt in the terminal. Deliberate bugs are clearly labelled; restore any classroom edits before proceeding.

Demo 6 introduces modules and returned pairs. Keep [study_helpers.py](study_helpers.py) beside it. Run the helper directly to demonstrate the main guard, then import it through demo 6.
