"""Demo 5: Combine data, decisions, and iteration."""

# PROBLEM
# Summarize four practice sessions. Attempt a solution before showing this worked example.
# These are practice rules, not a midterm exam or grading policy.
#
# INPUTS: Four nonnegative integer minute values.
# OUTPUTS: Total minutes and number of sessions reaching 30 minutes.
#
# PLAN (PSEUDOCODE)
# 1. Initialize total and target count.
# 2. Validate each of four entries with a retry loop.
# 3. Accumulate and count sessions of at least 30 minutes.

total_minutes = 0
target_sessions = 0
for session in range(1, 5):
    while True:
        try:
            minutes = int(input(f"Minutes for session {session}: "))
        except ValueError:
            print("Enter a whole number.")
            continue
        if minutes >= 0:
            break
        print("Minutes cannot be negative.")
    total_minutes = total_minutes + minutes
    if minutes >= 30:
        target_sessions = target_sessions + 1
print(f"Total minutes: {total_minutes}")
print(f"Sessions reaching the target: {target_sessions}")

# DESK CHECK
# 20, 30, 45, 0 gives 95 minutes and 2 target sessions.
#
# TRY IT: Include a negative number and text, then correct each entry.
# DISCUSS: Why does the validation loop sit inside the session loop?
