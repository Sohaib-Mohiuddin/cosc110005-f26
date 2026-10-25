"""Demo 6: Compare slices, sorted copies, and in-place sorting."""

# PROBLEM
# Select part of a practice-score list and compare two ways to sort it.
#
# INPUTS: An original list of numeric scores.
# OUTPUTS: A slice, a sorted copy, and the original list before and after sorting.
#
# PLAN (PSEUDOCODE)
# 1. Slice the first three scores.
# 2. Create a sorted copy with sorted().
# 3. Sort the original list in place with sort().

scores = [80, 60, 90, 70]
first_three = scores[:3]  # Stop index 3 is excluded.
first_three[0] = 100
print(f"Edited slice: {first_three}")
print(f"Original after slicing: {scores}")

ordered = sorted(scores)
print(f"Sorted copy: {ordered}")
print(f"Original after sorted(): {scores}")
result = scores.sort()
print(f"Original after sort(): {scores}")
print(f"Return value of sort(): {result}")
# Slices copy a flat list of numbers; nested mutable items still share references.

# DESK CHECK
# The edited slice is [100, 60, 90]; the original stays [80, 60, 90, 70].
# Both sorted lists are [60, 70, 80, 90], and sort() returns None.
#
# TRY IT: Try scores[1:3], scores[-2:], an empty list, and duplicate scores.
# DISCUSS: Why would scores = scores.sort() lose access to the sorted list?
