"""Midterm preparation 03: Trace reading progress."""

# WEEK 2 FOCUS: Tracing, accumulators, counters, and averages.
#
# WORK IN YOUR OWN FILE
# Copy this starter code into a new .py file in your own practice folder.
# Complete the TODO sections in your copy and test it with the cases below.
# The starter is intentionally incomplete; it does not yet solve the problem.
#
# PROBLEM
# A student records pages read during several sessions. Summarize the sessions.
#
# REQUIREMENTS
# 1. Use the supplied list; assume every entry is a nonnegative whole number.
# 2. Before coding, make a comment trace table with columns:
#    pages this session | running total | session count.
# 3. Visit each entry with a for loop, accumulating pages and counting sessions.
# 4. Print the running total after each session, then the final total and count.
# 5. Print the average pages per session to two decimal places only if count > 0.
#    Otherwise print "No reading sessions" without calculating an average.
# 6. Practise the algorithm explicitly: do not use sum() or len() for the totals.
# A session with zero pages still counts as a session.
#
# CHECK YOUR WORK
# [12, 18, 0, 10]: running totals 12, 30, 30, 40; count 4; average 10.00.
# [7]: total 7, count 1, average 7.00. []: No reading sessions.

# STARTER CODE
pages_read = [12, 18, 0, 10]
total_pages = 0
session_count = 0

# TODO: Add your predicted trace table here.

for pages in pages_read:
    # TODO: Update the total and count; display the running total.
    pass

# TODO: Display the summary and handle the empty-list case before division.
