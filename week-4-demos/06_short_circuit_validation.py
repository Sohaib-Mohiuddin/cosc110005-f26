"""Demo 6: Use short-circuit evaluation to guard an operation."""

# PROBLEM
# Check whether a nonempty class has at least 80 percent attendance.
#
# INPUTS: Whole-number enrolled and present counts stored in variables.
# OUTPUTS: A participation decision or an invalid-count message.
#
# PLAN (PSEUDOCODE)
# 1. Validate the counts.
# 2. Check for a nonempty class before division.
# 3. Report whether attendance reaches the target.

enrolled = 0
present = 0
if enrolled < 0 or present < 0 or present > enrolled:
    print("Use nonnegative counts with present no greater than enrolled.")
else:
    # and evaluates its right operand only when the left operand is true.
    meets_target = enrolled > 0 and present / enrolled >= 0.8
    if enrolled == 0:
        print("No enrolled students; attendance percentage is unavailable.")
    elif meets_target:
        print("Attendance target met.")
    else:
        print("Attendance is below the target.")

# DESK CHECK
# With both counts 0, no division occurs and no percentage is reported.
# With enrolled = 10, present = 8 meets the target; present = 7 does not.
#
# TRY IT: Try (10, 8), (10, 7), (0, 1), and (-1, 0) for enrolled and present.
# DISCUSS: Why would reversing the two operands of and cause a problem for an empty class?
