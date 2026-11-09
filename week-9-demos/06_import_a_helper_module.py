"""Demo 6: Reuse functions from a neighbouring module."""

# PROBLEM
# Use the companion study_helpers.py module from two callers without repeating its logic.
#
# INPUTS: Valid nonnegative whole-number minute values.
# OUTPUTS: Hours and remaining minutes.
#
# PLAN (PSEUDOCODE)
# 1. Import one function from the companion module.
# 2. Call it for two durations.
# 3. Unpack each returned pair and display it.

from study_helpers import split_minutes


def main():
    for duration in [135, 60]:
        hours, minutes = split_minutes(duration)
        print(f"{duration} minutes = {hours}h {minutes:02d}m")


if __name__ == "__main__":
    main()

# DESK CHECK
# 135 minutes = 2h 15m; 60 minutes = 1h 00m.
# The helper module imports without printing its own example.
#
# TRY IT: Run study_helpers.py directly, then run this demo. Compare the output.
# DISCUSS: Why does the helper module protect its example with an if __name__ guard?
