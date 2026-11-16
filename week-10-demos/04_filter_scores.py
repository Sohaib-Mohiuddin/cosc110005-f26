"""Demo 4: Build and return a new list."""

# PROBLEM
# Select scores meeting an example practice target while preserving input order.
#
# INPUTS: Valid scores and a target threshold.
# OUTPUTS: A new list of qualifying scores.
#
# PLAN (PSEUDOCODE)
# 1. Start an empty result list.
# 2. Append each qualifying score.
# 3. Return the completed list.

def scores_at_least(scores, threshold):
    """Return matching scores without modifying the input list."""
    matches = []
    for score in scores:
        if score >= threshold:
            matches.append(score)
    return matches


if __name__ == "__main__":
    scores = [55, 80, 60, 95, 80]
    selected = scores_at_least(scores, 80)
    print(f"Selected scores: {selected}")
    print(f"Original scores: {scores}")

# DESK CHECK
# Selected scores are [80, 95, 80]; duplicates and original order are preserved.
#
# TRY IT: Try thresholds of 0 and 101, then an empty list.
# DISCUSS: Why is building a new list easier to reason about than removing items while looping?
