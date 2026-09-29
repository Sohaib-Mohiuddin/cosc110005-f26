"""Demo 3: Accumulate values entered in a loop."""

# PROBLEM
# Total three days of study time. Assume valid, nonnegative integer entries.
#
# INPUTS: Three whole-number minute values.
# OUTPUTS: Running total and daily average.
#
# PLAN (PSEUDOCODE)
# 1. Initialize the total once.
# 2. Read and add each day's minutes.
# 3. Calculate the average after the loop.

total_minutes = 0
day_count = 3
for day in range(1, day_count + 1):
    minutes = int(input(f"Minutes for day {day}: "))
    total_minutes = total_minutes + minutes
    print(f"Running total: {total_minutes}")
average_minutes = total_minutes / day_count
print(f"Daily average: {average_minutes:.1f} minutes")

# DESK CHECK
# Inputs 20, 30, 40 give running totals 20, 50, 90 and average 30.0.
#
# TRY IT: Move the initialization inside the loop and explain the incorrect result.
# DISCUSS: Why calculate the final average after all entries have been processed?
