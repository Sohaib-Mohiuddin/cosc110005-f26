"""Demo 4: Use a trace to diagnose loop bounds."""

# PROBLEM
# Compare a loop that misses the final day with its corrected version.
#
# INPUTS: A five-day target.
# OUTPUTS: Two totals and a trace showing the missing value.
#
# PLAN (PSEUDOCODE)
# 1. Run the intentionally incorrect range.
# 2. Run the inclusive range.
# 3. Compare both results with the hand-calculated total.

last_day = 5
incorrect_total = 0
# INTENTIONAL BUG: range excludes last_day.
for day in range(1, last_day):
    incorrect_total = incorrect_total + day
print(f"Incorrect total: {incorrect_total}")

correct_total = 0
for day in range(1, last_day + 1):
    correct_total = correct_total + day
    print(f"day={day}, total={correct_total}")
print(f"Correct total: {correct_total}")

# DESK CHECK
# Incorrect total: 10. Correct trace totals: 1, 3, 6, 10, 15.
#
# TRY IT: Set last_day to 1. Explain why this exposes the bug quickly.
# DISCUSS: Is a program that runs without an exception necessarily correct?
