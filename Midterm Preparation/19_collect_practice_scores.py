"""Midterm preparation 19: Collect practice scores."""

# WEEK 5 FOCUS: Sentinels, validation, totals, and safe averages.
#
# WORK IN YOUR OWN FILE
# Copy this starter code into a new .py file in your own practice folder.
# Complete the TODO sections in your copy and test it with the cases below.
# The starter is intentionally incomplete; it does not yet solve the problem.
#
# PROBLEM
# Accept an unknown number of practice scores and stop when the student enters done.
#
# REQUIREMENTS
# 1. Read and strip each entry; recognize done regardless of capitalization.
# 2. Check for the sentinel BEFORE trying to convert the entry to an integer.
# 3. Accept integer scores from 0 through 100 inclusive. Use try/except ValueError
#    for non-integer text and a separate range check for out-of-range integers.
# 4. Invalid entries produce an explanation but change neither total nor count.
# 5. Read another entry on every non-sentinel path, including invalid entries.
# 6. At the end, display valid-score count and average to two decimal places.
#    With no valid scores, print "No scores entered" and do not divide.
# 7. Use a while loop, an accumulator, and a counter; no list is required.
#
# CHECK YOUR WORK
# 80, bad, -1, 100, done: count 2 and average 90.00.
# 0, 100, " DONE ": count 2 and average 50.00; zero is a valid score.
# done immediately, or bad then done: No scores entered.
# 3.5, 101, done: both scores rejected; no average is calculated.

# STARTER CODE
total_score = 0
score_count = 0
entry = input("Practice score (0-100), or done: ").strip().lower()

# TODO: Add a while loop that stops on done.
# Inside it, convert and validate; update totals only for valid scores.
# Remember to prompt again after BOTH accepted and rejected entries.

# TODO: Display the count and either the average or the no-scores message.
