"""Demo 3: Trace counter and accumulator changes."""

# PROBLEM
# Award one more practice point on each successive day.
#
# INPUTS: A nonnegative number of days.
# OUTPUTS: A trace and total points.
#
# PLAN (PSEUDOCODE)
# 1. Initialize the counter and total.
# 2. Add the current day number.
# 3. Advance the day and repeat while within the limit.

days = 4
day = 1
total_points = 0
print("day | total before | total after")
while day <= days:
    before = total_points
    total_points = total_points + day
    print(f"{day:3} | {before:12} | {total_points:11}")
    day = day + 1
print(f"Total points: {total_points}")

# DESK CHECK
# Rows end with totals 1, 3, 6, 10. After the loop day is 5.
#
# TRY IT: Predict the output for days = 0 and days = 1.
# DISCUSS: Which values change on each iteration, and which stay constant?
