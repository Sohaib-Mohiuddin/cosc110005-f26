"""Demo 1: Review conversion and formatted output."""

# PROBLEM
# Convert a nonnegative whole number of minutes into hours and minutes.
#
# INPUTS: A duration in minutes.
# OUTPUTS: Hours and leftover minutes, or an error.
#
# PLAN (PSEUDOCODE)
# 1. Convert the input.
# 2. Reject negative durations.
# 3. Use quotient and remainder for the result.

try:
    total_minutes = int(input("Duration in minutes: "))
except ValueError:
    print("Enter a whole number.")
else:
    if total_minutes < 0:
        print("Duration cannot be negative.")
    else:
        hours = total_minutes // 60
        minutes = total_minutes % 60
        print(f"Duration: {hours}h {minutes:02d}m")

# DESK CHECK
# 135 gives 2h 15m; 60 gives 1h 00m; 0 gives 0h 00m.
#
# TRY IT: Check 59, 60, 61, -1, and abc.
# DISCUSS: Which cases check arithmetic boundaries and which check validation?
