# Week 3: Working with data

Variables, types, conversion, arithmetic, strings, and formatting.

Five core Python demos plus an optional extension for the professor to present in numerical order. Each file includes a problem, inputs and outputs, pseudocode, a desk check, and a try-it/discussion prompt.

## Run

From the repository root, using Python 3:

```bash
python3 week-3-demos/01_explore_data_types.py
```

Replace the filename to run another demo. On Windows, `py` can be used in place of `python3`. No pip packages are required.

## Teaching sequence

| Demo | Focus |
| --- | --- |
| [01_explore_data_types.py](01_explore_data_types.py) | Choose types and meaningful variable names |
| [02_convert_keyboard_input.py](02_convert_keyboard_input.py) | Convert input text into numbers |
| [03_use_arithmetic_operators.py](03_use_arithmetic_operators.py) | Use division, remainder, and precedence |
| [04_clean_and_format_text.py](04_clean_and_format_text.py) | Clean and format strings |
| [05_print_a_receipt.py](05_print_a_receipt.py) | Calculate and format a small receipt |
| [06_explore_decimal_precision.py](06_explore_decimal_precision.py) | Optional extension: Distinguish stored values from display formatting |

## Classroom flow

1. Read the problem and ask students to identify inputs, processing, and outputs.
2. Trace the pseudocode and predict the desk-check result before running.
3. Run the demo, then change one input or requirement at a time.
4. Use the try-it and discussion prompts to check understanding.

Hardcoded inputs are near the top of early demos or in the guarded demonstration block in later demos. Interactive scripts prompt in the terminal. Deliberate bugs are clearly labelled; restore any classroom edits before proceeding.

Demo 2 deliberately assumes valid numeric input so conversion can be taught before error handling. Demo 5 assumes the fixed discount does not exceed the subtotal. Discuss these preconditions; week 4 introduces validation.
