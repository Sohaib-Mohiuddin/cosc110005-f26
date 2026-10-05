"""Demo 2: Trace nested loops with a seating chart."""

# PROBLEM
# Print seat labels for three rows with four seats each.
#
# INPUTS: Positive row and seat counts.
# OUTPUTS: Twelve seat labels.
#
# PLAN (PSEUDOCODE)
# 1. Loop through row numbers.
# 2. For each row, loop through seat numbers.
# 3. Start a new line after each row.

row_count = 3
seats_per_row = 4
for row in range(1, row_count + 1):
    for seat in range(1, seats_per_row + 1):
        print(f"R{row}S{seat}", end=" ")
    print()  # This runs once per row, after the inner loop.

# DESK CHECK
# First row: R1S1 R1S2 R1S3 R1S4. There are 3 * 4 = 12 labels.
#
# TRY IT: Use two rows and three seats. Count inner-loop repetitions.
# DISCUSS: What changes if the final print() is indented inside the inner loop?
