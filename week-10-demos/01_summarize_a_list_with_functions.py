"""Demo 1: Pass a collection to a function."""

# PROBLEM
# Calculate an average without modifying the scores supplied by the caller.
#
# INPUTS: A possibly empty list of valid numeric scores.
# OUTPUTS: An average, or a no-scores message.
#
# PLAN (PSEUDOCODE)
# 1. Return None for an empty list.
# 2. Accumulate scores and return their average.
# 3. Let the caller choose how to display the result.

def average_score(scores):
    """Return the mean, or None when there are no scores."""
    if len(scores) == 0:
        return None
    total = 0
    for score in scores:
        total = total + score
    return total / len(scores)


scores = [70, 80, 90, 99, 10, 40, 70, 35, 70.2]
average = average_score(scores)
if average is None:
    print("No scores available.")
else:
    print(f"Average: {average:.2f}")
print(f"Original scores: {scores}")

# DESK CHECK
# The average is 80.00 and the original list remains [70, 80, 90].
#
# TRY IT: Try [] and [0]. Explain how their results differ.
# DISCUSS: Why would returning 0 for an empty list be ambiguous?
