"""Demo 3: Traverse a list to calculate statistics."""

# PROBLEM
# Find the total, average, and highest score without hiding the traversal.
#
# INPUTS: A possibly empty list of valid numeric scores.
# OUTPUTS: A summary or an empty-list message.
#
# PLAN (PSEUDOCODE)
# 1. Handle an empty list first.
# 2. Initialize highest from the first element.
# 3. Traverse to update total and highest, then calculate the average.

scores = [65, 90, 75, 90]
if len(scores) == 0:
    print("No scores to summarize.")
else:
    total = 0
    highest = scores[0]
    for index in range(len(scores)):
        score = scores[index]
        total = total + score
        if score > highest:
            highest = score
        print(f"Index {index}: score {score}")
    print(f"Total: {total}; average: {total / len(scores):.2f}; highest: {highest}")

# DESK CHECK
# Total 320, average 80.00, highest 90. Valid indices are 0 through 3.
#
# TRY IT: Try [], [50], and [100, 0].
# DISCUSS: Why initialize highest from the data instead of an arbitrary number?
