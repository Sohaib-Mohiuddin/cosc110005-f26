"""Demo 2: Review mutually exclusive decisions."""

# PROBLEM
# Recommend a lab activity based on readiness and available time.
#
# INPUTS: A readiness Boolean and nonnegative minutes.
# OUTPUTS: One activity recommendation.
#
# PLAN (PSEUDOCODE)
# 1. Validate the available time.
# 2. Check whether setup is complete.
# 3. Choose an activity by available time.

setup_complete = True
minutes = 25
if minutes < 0:
    activity = "Enter a nonnegative time."
elif not setup_complete:
    activity = "Finish the environment setup."
elif minutes >= 30:
    activity = "Build a complete practice solution."
elif minutes >= 10:
    activity = "Trace and modify one demo."
else:
    activity = "Write a question for the next class."
print(activity)

# DESK CHECK
# Ready with 25 minutes selects Trace and modify one demo.
#
# TRY IT: Check 9, 10, 29, 30, then repeat with setup_complete = False.
# DISCUSS: Which requirement has priority when setup is incomplete?
