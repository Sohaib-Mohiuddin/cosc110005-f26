"""Demo 7: Use the outer-loop value to control the inner loop."""

# PROBLEM
# Print a triangle whose first row has one star, second row has two, and so on.
# Use nested loops so we can trace when each individual star is printed.
#
# INPUTS: A positive integer row count, set below.
# OUTPUTS: A left-aligned triangle of stars.
#
# PLAN (PSEUDOCODE)
# 1. Visit each row number from 1 through row_count.
# 2. For that row, print one star for each position from 1 through row.
# 3. Move to a new line after all stars in that row have been printed.

row_count = 44

# range stops BEFORE its second argument, so + 1 includes the final row.
for row in range(1, row_count + 1):
    # The inner loop starts again at 1 for every new row.
    # row stays fixed while position changes; this row gets exactly row stars.
    for position in range(1, row + 1):
        print("*", end=" ")  # An empty end keeps the next star on the same line.

    # Inside the outer loop, but OUTSIDE the inner loop: one newline per row.
    print()

# DESK CHECK (row_count = 4)
# row    position values    stars printed on this row
# 1      1                  *
# 2      1, 2               **
# 3      1, 2, 3            ***
# 4      1, 2, 3, 4         ****
# The outer loop runs 4 times; the inner body runs 1 + 2 + 3 + 4 = 10 times.
# Notice that the inner loop does NOT run the same number of times each row.
#
# EXPECTED OUTPUT
# *
# **
# ***
# ****
#
# TRY IT: Set row_count to 1, then 5. Predict the output and total star count.
# TRY IT: Replace row + 1 with row_count + 1 in the inner range. Predict the shape.
# DISCUSS: Why must print() be after the inner loop but still inside the outer loop?
