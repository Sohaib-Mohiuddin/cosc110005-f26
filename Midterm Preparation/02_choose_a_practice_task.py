"""Midterm preparation 02: Choose a practice task."""

# WEEK 2 FOCUS: Selection algorithms and boundary tracing.
#
# WORK IN YOUR OWN FILE
# Copy this starter code into a new .py file in your own practice folder.
# Complete the TODO sections in your copy and test it with the cases below.
# The starter is intentionally incomplete; it does not yet solve the problem.
#
# PROBLEM
# Recommend exactly one practice task based on the time a student has available.
#
# REQUIREMENTS
# 1. Use the integer minutes_available supplied below; no keyboard input needed.
# 2. Negative time: display "Invalid time".
# 3. At least 45 minutes: display "Complete a practice exercise".
# 4. From 20 through 44 minutes: display "Trace a program".
# 5. From 5 through 19 minutes: display "Review key terms".
# 6. From 0 through 4 minutes: display "Plan your next session".
# 7. Write pseudocode in comments and implement an if/elif/else chain.
# Choose the order carefully so exactly one message is printed.
#
# CHECK YOUR WORK
# 30 -> Trace a program; 45 -> Complete a practice exercise.
# Test -1, 0, 4, 5, 19, 20, 44, and 45 and record the chosen branch in comments.
# Explain why testing "at least 5" first can give an incorrect recommendation.

# STARTER CODE
minutes_available = 30

# TODO: Write a numbered decision plan here.

# TODO: Replace pass with the first message, then add the remaining branches.
if minutes_available < 0:
    pass
