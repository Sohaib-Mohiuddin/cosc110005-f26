# Week 8: Arrays

Use Python lists for array concepts: indexing, updates, traversal, search, and two-dimensional data.

Five core Python demos plus an optional extension for the professor to present in numerical order. Each file includes a problem, inputs and outputs, pseudocode, a desk check, and a try-it/discussion prompt.

## Run

From the repository root, using Python 3:

```bash
python3 week-8-demos/01_index_and_update_a_list.py
```

Replace the filename to run another demo. On Windows, `py` can be used in place of `python3`. No pip packages are required.

## Teaching sequence

| Demo | Focus |
| --- | --- |
| [01_index_and_update_a_list.py](01_index_and_update_a_list.py) | Use a Python list as an array-like collection |
| [02_add_and_remove_items.py](02_add_and_remove_items.py) | Change the size of a list |
| [03_traverse_and_summarize.py](03_traverse_and_summarize.py) | Traverse a list to calculate statistics |
| [04_search_for_a_student.py](04_search_for_a_student.py) | Return the position of the first match |
| [05_read_a_two_dimensional_list.py](05_read_a_two_dimensional_list.py) | Traverse rows and columns |
| [06_slice_and_sort_lists.py](06_slice_and_sort_lists.py) | Optional extension: Compare slices, sorted copies, and in-place sorting |

## Classroom flow

1. Read the problem and ask students to identify inputs, processing, and outputs.
2. Trace the pseudocode and predict the desk-check result before running.
3. Run the demo, then change one input or requirement at a time.
4. Use the try-it and discussion prompts to check understanding.

Hardcoded inputs are near the top of early demos or in the guarded demonstration block in later demos. Interactive scripts prompt in the terminal. Deliberate bugs are clearly labelled; restore any classroom edits before proceeding.

Python lists are dynamic collections, not fixed-size typed arrays. These examples use homogeneous lists to teach the array concepts in the course topic. No NumPy or other external array library is needed.
