# Assignment 1: Worked solution and teaching notes

This instructor-requested example demonstrates how to move from the Assignment 1 requirements to a plan, working code, and testing. Read it alongside the [assignment brief](brief.md) and [original PDF](COSC1100.Assignment1.SquareNumbers.pdf).

Open the [documented Python solution](square_numbers_solution.py) to read the description, inputs, outputs, pseudocode, and desk checks above the code. The program and these notes were prepared with OpenAI Codex for classroom review. Follow your instructor's directions when using this example in your own work.

## Problem description

Ask for two whole-number bounds and display every square number within that inclusive range. For each result, also display the whole-number root: `25 (5 squared)` means `5 * 5 = 25`.

The bounds apply to the square numbers being displayed. For bounds 4 and 120, display squares from 4 through 100; do not square every number from 4 through 120. A valid range can contain no squares.

## Inputs, processing, and outputs

| Part | What the program does |
| --- | --- |
| Lower bound | Accept an integer from 1 through 10000, including both endpoints. |
| Upper bound | Accept an integer from the accepted lower bound through 10000. |
| Validation | Retry the affected bound after text, decimal input, or an out-of-range integer. |
| Processing | Generate `1 * 1`, `2 * 2`, `3 * 3`, and so on, stopping when the square exceeds the upper bound. |
| Results | Print a banner containing the accepted bounds and each qualifying square with its root. |
| Empty result | Print a clear message when a valid range contains no squares. |
| Finish | Wait for an Enter key press. |

`int(input(...))` rejects entries such as `Chicken`, `4.5`, and `4.0`. The program asks for integer text; it does not convert through `float()` and silently discard a decimal part. Spaces around an integer, such as ` 4 `, are accepted.

## Plan before coding

1. Display the opening banner.
2. Repeat the lower-bound prompt until conversion and range checks both succeed.
3. Repeat the upper-bound prompt until conversion and range checks both succeed. Keep the accepted lower bound while retrying the upper bound.
4. Display a results banner containing both valid bounds.
5. Start with root 1 and square 1. Generate squares in increasing order while the square is no greater than the upper bound.
6. Print each generated square that is at least the lower bound, together with its root.
7. Display an explanatory message if no square was printed.
8. Wait for Enter before finishing.

The complete pseudocode is in the comments above the implementation. There are three `while` loops: lower-bound validation, upper-bound validation, and square generation. The five functions separate the banner, the two input stages, result generation, and program coordination. Functions are also consistent with the handout's AI-use instruction; its requested word appears in a source comment.

## Why the square-generation loop works

Every positive square has a positive whole-number root. Trying roots 1, 2, 3, and so on produces each possible square exactly once, in order. Once a square exceeds the upper bound, every later square will exceed it too. At most 100 roots need to be examined because the largest allowed bound is 10000 and `100 * 100 = 10000`.

The loop condition uses `<=`, and the lower-bound check uses `>=`, so a square equal to either boundary is included. Incrementing `root` on every iteration ensures the loop progresses even while generated squares are below the lower bound. Integer multiplication supplies the square and its exact root without floating-point comparisons.

### Trace: bounds 5 and 10

The table shows the values before each attempt to enter the loop body.

| Root | Square | Square <= 10? | Square >= 5? | Action |
| --- | --- | --- | --- | --- |
| 1 | 1 | Yes | No | Skip; advance to root 2. |
| 2 | 4 | Yes | No | Skip; advance to root 3. |
| 3 | 9 | Yes | Yes | Print `9 (3 squared)`; advance to root 4. |
| 4 | 16 | No | Not evaluated | Stop the loop. |

## Run on your computer

From the repository's root folder, run:

```text
python3 Assignment-1/square_numbers_solution.py
```

On Windows, use:

```text
py Assignment-1/square_numbers_solution.py
```

Enter each bound when prompted, then press Enter at the closing prompt.

## Run on the course site

Open the [Python solution](square_numbers_solution.py), expand **Try Python in your browser**, and enter the following in **Program input**, one answer per line:

```text
4
120

```

Include the final blank line after `120`: it supplies the empty answer for **Press Enter to exit**. Click **Run**. In this browser runner, supply all answers before running, including replacement values for any invalid entries. A message about running out of input means another answer is needed.

You can also use **Run sample checks** to try the handout's range, empty results, equal bounds, and invalid inputs. These checks provide practice feedback; the test plan below covers additional cases. Use **Trace code** with a small range such as 5 through 10 to step through execution.

## Sample run: the handout's range

```text
************************************************************************
                          SQUARE NUMBER FINDER
************************************************************************

Please enter the lower bound: 4
Please enter the upper bound: 120

************************************************************************
                     Square Numbers Between 4 and 120
************************************************************************
4 (2 squared)
9 (3 squared)
16 (4 squared)
25 (5 squared)
36 (6 squared)
49 (7 squared)
64 (8 squared)
81 (9 squared)
100 (10 squared)

Press Enter to exit...
```

### Sample validation sequence

The following excerpt shows the input stage. Entering invalid upper bounds does not restart the lower-bound prompt.

```text
Please enter the lower bound: Chicken
Invalid input: Please enter a whole number.

Please enter the lower bound: 4.5
Invalid input: Please enter a whole number.

Please enter the lower bound: 10001
Invalid input: Please enter a number between 1 and 10000.

Please enter the lower bound: 4
Please enter the upper bound: 3
Invalid input: Please enter a number between 4 and 10000.

Please enter the upper bound: 120
```

For bounds 10 and 15, the result section contains `No square numbers were found in this range.` A range with no squares is valid input.

## Test plan

After each valid range, confirm that the program waits at **Press Enter to exit**. Compare every result, its order, and its root; checking only the first and last results can miss errors.

| Test | Entries or bounds | Expected behaviour |
| --- | --- | --- |
| Handout example | 4, 120 | Exactly nine squares: 4, 9, 16, 25, 36, 49, 64, 81, 100. |
| Smallest range | 1, 1 | Only `1 (1 squared)`. |
| Largest equal bounds | 10000, 10000 | Only `10000 (100 squared)`. |
| Full allowed range | 1, 10000 | Exactly 100 results, roots 1 through 100. |
| Both endpoints square | 4, 9 | Include both `4 (2 squared)` and `9 (3 squared)`. |
| Non-square endpoints | 5, 10 | Only `9 (3 squared)`. |
| Empty result | 10, 15 | No-square message; no result rows. |
| Equal non-square bounds | 2, 2 | No-square message. |
| Equal square bounds | 16, 16 | Only `16 (4 squared)`. |
| Text or empty lower entry | `Chicken` or an empty line, then 4 | Whole-number error; retry the lower bound. |
| Decimal lower entry | `4.5` or `4.0`, then 4 | Whole-number error; retry the lower bound. |
| Lower out of range | -1, 0, 10001, then 4 | Range error after each invalid integer. |
| Text or decimal upper entry | Lower 4; `hello`, `5.5`, then 120 | Whole-number errors; retain lower 4. |
| Upper below lower | Lower 4; upper 3, then 120 | Error stating the allowed range is 4 through 10000. |
| Upper above maximum | Lower 4; upper 10001, then 120 | Range error; retry only the upper bound. |
| Surrounding spaces | ` 4 `, ` 9 ` | Accept both and print 4 and 9. |
| Several errors in succession | Text, decimal, invalid range, then valid input | Keep retrying; do not generate results before both bounds are valid. |

The repository also contains automated checks for complete result sets, validation retries, boundary values, and the final pause. Run them from the repository root with `python3 -m unittest discover -s site -p 'test_assignment1_solution.py' -v`.

## Classroom discussion

- Why is zero excluded even though `0 * 0` is a square? The assignment sets the smallest permitted lower bound to 1.
- What changes if the generation loop uses `<` instead of `<=`? A square equal to the upper bound would be omitted.
- What happens if the root update is placed inside the `if`? A range starting above 1 could cause the loop to stop progressing.
- Why catch `ValueError` specifically? Invalid integer text causes that exception; other failures should not be disguised as invalid input.
- Which two functions have similar validation logic? As a follow-up exercise, combine them into a reusable bounded-integer input function while preserving the same behaviour.
- How would you test that there are no extra squares, duplicates, or incorrect roots? Compare the complete result rows with the expected list.
