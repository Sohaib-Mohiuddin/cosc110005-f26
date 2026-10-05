"""Demo 3: Distinguish skipping from stopping."""

# PROBLEM
# Inspect supplied practice scores, skip invalid scores, and stop at -1.
#
# INPUTS: A fixed list of readings; -1 is the stop marker.
# OUTPUTS: Valid scores processed before the marker.
#
# PLAN (PSEUDOCODE)
# 1. Visit each reading.
# 2. Stop at -1; skip other out-of-range values.
# 3. Count and display valid scores.

readings = [70, 105, 80, -1, 90]
accepted_count = 0
for score in readings:
    if score == -1:
        break
    if score < 0 or score > 100:
        print(f"Skipping invalid score: {score}")
        continue
    accepted_count = accepted_count + 1
    print(f"Accepted: {score}")
print(f"Accepted count: {accepted_count}")

# DESK CHECK
# 70 and 80 are accepted; 105 is skipped; -1 stops before 90. Count is 2.
#
# TRY IT: Move -1 to the beginning or remove it.
# DISCUSS: How would replacing continue with break change the result?
