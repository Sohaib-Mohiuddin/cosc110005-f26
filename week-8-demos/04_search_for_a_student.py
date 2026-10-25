"""Demo 4: Return the position of the first match."""

# PROBLEM
# Locate the first matching student name using a linear search.
#
# INPUTS: A roster and a target name.
# OUTPUTS: The first matching index or a missing-name message.
#
# PLAN (PSEUDOCODE)
# 1. Use -1 to represent no match.
# 2. Compare each name with the target.
# 3. Save the first matching index and stop.

roster = ["Alex", "Sam", "Jordan", "Sam"]
target = "Sam"
found_index = -1
for index in range(len(roster)):
    if roster[index] == target:
        found_index = index
        break
if found_index == -1:
    print(f"{target} is not on the roster.")
else:
    print(f"First match at index {found_index}: {roster[found_index]}")

# DESK CHECK
# Sam is found at index 1. The later Sam at index 3 is never checked.
#
# TRY IT: Search for Alex, Jordan, and Taylor; also try an empty roster.
# DISCUSS: Why must we check for -1 before using it as an index in Python?
