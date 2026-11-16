"""Demo 5: Combine nested lists with reusable functions."""

# PROBLEM
# Calculate a total for each student's quiz row.
#
# INPUTS: A list of numeric rows, which may have different lengths.
# OUTPUTS: A list of row totals.
#
# PLAN (PSEUDOCODE)
# 1. Write a function to total one row.
# 2. Call it for every row.
# 3. Return and display the resulting totals.

def total_row(row):
    """Return a row total; an empty row totals zero."""
    total = 0
    for value in row:
        total = total + value
    return total


def student_totals(score_rows):
    """Return one total per row without changing the table."""
    totals = []
    for row in score_rows:
        totals.append(total_row(row))
    return totals


if __name__ == "__main__":
    table = [[70, 80], [90, 85], []]
    totals = student_totals(table)
    for index in range(len(totals)):
        print(f"Student {index + 1}: {totals[index]}")

# DESK CHECK
# Totals are [150, 175, 0]. An empty outer list returns [].
#
# TRY IT: Add a third quiz to only the first row.
# DISCUSS: Which function is responsible for visiting rows, and which visits individual scores?
