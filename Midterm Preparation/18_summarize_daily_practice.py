"""Midterm preparation 18: Summarize daily practice."""

# WEEK 5 FOCUS: Input loops, accumulators, and conditional counters.
#
# WORK IN YOUR OWN FILE
# Copy this starter code into a new .py file in your own practice folder.
# Complete the TODO sections in your copy and test it with the cases below.
# The starter is intentionally incomplete; it does not yet solve the problem.
#
# PROBLEM
# Summarize five days of practice time and count days that met a daily goal.
#
# REQUIREMENTS
# 1. Use a for loop to ask for practice minutes on each of five numbered days.
# 2. Assume every entry is a valid nonnegative whole number; no retries needed.
# 3. Accumulate total minutes and count days with at least 30 minutes of practice.
# 4. Print the running total after each entry.
# 5. After the loop, display total minutes, daily average to one decimal place,
#    and number of days meeting the goal. Zero-minute days count in the average.
# 6. Keep total and counter initialization outside the loop. Do not store a list.
#
# CHECK YOUR WORK
# 20, 30, 45, 0, 55: running totals 20, 50, 95, 95, 150;
# final total 150, average 30.0, days meeting the goal 3.
# Five zero entries: total 0, average 0.0, goal days 0.
# Five entries of 30: total 150, average 30.0, goal days 5.

# STARTER CODE
day_count = 5
daily_goal = 30
total_minutes = 0
goal_days = 0

for day in range(1, day_count + 1):
    # TODO: Prompt for this day's minutes, update totals, and show progress.
    pass

# TODO: Display the final total, average, and goal-day count.
