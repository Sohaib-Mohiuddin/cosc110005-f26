"""Midterm preparation 04: Find a required supply."""

# WEEK 2 FOCUS: Linear search, Boolean flags, and comparison counts.
#
# WORK IN YOUR OWN FILE
# Copy this starter code into a new .py file in your own practice folder.
# Complete the TODO sections in your copy and test it with the cases below.
# The starter is intentionally incomplete; it does not yet solve the problem.
#
# PROBLEM
# Check whether a supply box contains a required classroom item.
#
# REQUIREMENTS
# 1. Search the supplied list one item at a time using a for loop.
# 2. Count every comparison, including the comparison that finds a match.
# 3. Compare exact strings: "Marker" and "marker" are different in this exercise.
# 4. On the first match, set found to True and stop using break.
# 5. Print "Supply found" or "Supply missing", then the comparison count.
# 6. Do not use the in operator as a shortcut for searching the list.
# 7. Write a short pseudocode plan and predict the count before running.
#
# CHECK YOUR WORK
# Required "marker": found after 3 comparisons.
# Required "paper": found after 1; "tape": found after 4; "ruler": missing after 4.
# An empty list reports missing after 0 comparisons.
# If there are two copies of an item, stop at the first one.

# STARTER CODE
supplies = ["paper", "pencil", "marker", "tape"]
required_supply = "marker"
found = False
comparisons = 0

# TODO: Write your search plan and predicted comparison count here.

for supply in supplies:
    # TODO: Count the comparison, check for a match, and stop when found.
    pass

# TODO: Report the result and number of comparisons.
