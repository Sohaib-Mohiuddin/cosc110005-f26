"""Midterm preparation 17: Reach a reading goal."""

# WEEK 5 FOCUS: Condition-controlled loops and termination.
#
# WORK IN YOUR OWN FILE
# Copy this starter code into a new .py file in your own practice folder.
# Complete the TODO sections in your copy and test it with the cases below.
# The starter is intentionally incomplete; it does not yet solve the problem.
#
# PROBLEM
# Count how many additional reading sessions are needed to reach a page target.
#
# REQUIREMENTS
# 1. Use the supplied whole-number target, pages already read, and pages per session.
#    Assume target and pages already read are nonnegative.
# 2. If the target is already reached or exceeded, report zero additional sessions.
# 3. Otherwise, if pages_per_session is zero or negative, print a helpful error.
# 4. Otherwise, use a while loop to add one session's pages until target is reached
#    OR exceeded. Increase the session counter on every repetition.
# 5. Print a progress line per session, then final pages and sessions required.
# 6. Do not divide to calculate the session count; practise condition-controlled loops.
#
# CHECK YOUR WORK
# Target 50, already read 8, rate 12: progress 20, 32, 44, 56; 4 sessions.
# Target 44 with the other defaults: 3 sessions and 44 pages.
# Already read 50 or more: 0 sessions, even if the rate is zero.
# Target not yet reached with rate 0 or -2: error; the program must not loop forever.

# STARTER CODE
target_pages = 50
pages_read = 8
pages_per_session = 12
sessions = 0

# TODO: Handle an already-reached target before checking the reading rate.

# TODO: For a valid remaining goal, write a while loop that updates both
# pages_read and sessions. Do not run an unfinished while loop without updates.

# TODO: Display progress and the appropriate final result.
