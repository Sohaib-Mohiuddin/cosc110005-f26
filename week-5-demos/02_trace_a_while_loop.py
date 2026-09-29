"""Demo 2: Track progress toward a loop condition."""

# PROBLEM
# Count practice sessions needed to complete a set of problems.
#
# INPUTS: Problem target and a positive number completed each session.
# OUTPUTS: Progress trace and session count.
#
# PLAN (PSEUDOCODE)
# 1. Start completed work and sessions at zero.
# 2. Repeat until the target is reached.
# 3. Update both values every time.

target = 17  # Assume a nonnegative target.
problems_per_session = 5
completed = 0
sessions = 0
if problems_per_session <= 0:
    print("Complete at least one problem per session.")
else:
    while completed < target:
        completed = completed + problems_per_session
        sessions = sessions + 1
        print(f"Session {sessions}: {completed} problems completed")
    print(f"Sessions needed: {sessions}")

# DESK CHECK
# Completed values are 5, 10, 15, 20. Four sessions are needed.
#
# TRY IT: Try targets of 0 and 20, then a rate of 0.
# DISCUSS: Which update prevents an infinite loop?
