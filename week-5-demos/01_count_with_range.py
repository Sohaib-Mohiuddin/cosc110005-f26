"""Demo 1: Repeat a known number of times."""

# PROBLEM
# Display a five-day study plan and a countdown.
#
# INPUTS: A fixed number of study days.
# OUTPUTS: Day numbers and countdown values.
#
# PLAN (PSEUDOCODE)
# 1. Count from 1 through 5.
# 2. Count backwards from 3 through 1.
# 3. Display the start message.

for day in range(1, 6):
    # The stop value 6 is excluded.
    print(f"Day {day}: practise for 20 minutes.")
for remaining in range(3, 0, -1):
    print(remaining)
print("Begin!")

# DESK CHECK
# Days: 1, 2, 3, 4, 5. Countdown: 3, 2, 1, then Begin!
#
# TRY IT: Use range(2, 11, 2). Predict which numbers appear.
# DISCUSS: Why does range(5) begin at zero?
