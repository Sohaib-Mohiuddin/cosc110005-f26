"""Demo 1: Use a Python list as an array-like collection."""

# PROBLEM
# Store and update three practice scores. Python lists are resizable;
# we use one element type here to practise introductory array concepts.
#
# INPUTS: A list of scores.
# OUTPUTS: First and last scores and the updated list.
#
# PLAN (PSEUDOCODE)
# 1. Read elements by zero-based index.
# 2. Replace the second element.
# 3. Display the list length and contents.

scores = [70, 80, 90]
print(f"First score: {scores[0]}")
print(f"Last score: {scores[-1]}")
scores[1] = 85
print(f"Updated scores: {scores}")
print(f"Score count: {len(scores)}")
# With three elements, valid nonnegative indices are 0, 1, and 2.

# DESK CHECK
# First is 70; last is 90; updated list is [70, 85, 90]; length is 3.
#
# TRY IT: Predict scores[3], then run it and inspect the IndexError.
# DISCUSS: How does an element's index differ from its value?
