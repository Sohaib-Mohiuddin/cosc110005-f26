"""Demo 6: Trace a sorting algorithm through a function."""

# PROBLEM
# Sort a short score list by repeatedly selecting the smallest remaining value.
# This explicit algorithm is for tracing; sorted() is the usual Python choice.
#
# INPUTS: A possibly empty list of numeric scores.
# OUTPUTS: A trace and a sorted copy, leaving the original unchanged.
#
# PLAN (PSEUDOCODE)
# 1. Copy the supplied list.
# 2. For each position, find the smallest remaining value.
# 3. Swap it into position and display the current state.

def selection_sorted(values):
    """Return a sorted copy and print each completed selection pass."""
    result = values.copy()
    for start in range(len(result) - 1):
        smallest = start
        for index in range(start + 1, len(result)):
            if result[index] < result[smallest]:
                smallest = index
        # Save one value so replacing it does not lose it before the swap.
        saved = result[start]
        result[start] = result[smallest]
        result[smallest] = saved
        print(f"Pass {start + 1}: {result}")
    return result


if __name__ == "__main__":
    scores = [80, 60, 90, 70]
    ordered = selection_sorted(scores)
    print(f"Sorted copy: {ordered}")
    print(f"Original: {scores}")

# DESK CHECK
# Passes: [60, 80, 90, 70], [60, 70, 90, 80], [60, 70, 80, 90].
# The original stays [80, 60, 90, 70].
#
# TRY IT: Try [], [50], [70, 70, 60], and an already-sorted list.
# DISCUSS: How many comparisons does the inner loop make on each pass?
