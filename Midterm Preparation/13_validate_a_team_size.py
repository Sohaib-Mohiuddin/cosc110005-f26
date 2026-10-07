"""Midterm preparation 13: Validate a team size."""

# WEEK 4 FOCUS: Conversion errors versus range errors.
#
# WORK IN YOUR OWN FILE
# Copy this starter code into a new .py file in your own practice folder.
# Complete the TODO sections in your copy and test it with the cases below.
# The starter is intentionally incomplete; it does not yet solve the problem.
#
# PROBLEM
# Accept one proposed team size for a classroom activity.
#
# REQUIREMENTS
# 1. Read and strip one input string. A valid team has 2 through 6 people.
# 2. Use int() inside try/except ValueError to handle non-integer text.
# 3. If conversion fails, print "Enter a whole number".
# 4. If conversion succeeds but the size is outside 2-6, print "Choose 2 to 6 people".
# 5. Otherwise print "Team accepted: <size> people".
# 6. Print exactly one result and then end. Do not add a retry loop.
# 7. Keep range validation separate from conversion error handling.
#
# CHECK YOUR WORK
# "4" and " 4 " -> Team accepted: 4 people. Both 2 and 6 are accepted.
# "1" and "7" -> Choose 2 to 6 people.
# "four", "3.5", and an empty input -> Enter a whole number; no traceback.

# STARTER CODE
team_text = input("Team size (2-6): ").strip()

try:
    # TODO: Convert team_text and store team_size.
    pass
except ValueError:
    # TODO: Display the conversion error message.
    pass
else:
    # TODO: Check the allowed range and print acceptance or a range error.
    pass
