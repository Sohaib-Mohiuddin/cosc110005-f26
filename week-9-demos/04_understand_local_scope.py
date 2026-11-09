"""Demo 4: Distinguish local values from caller values."""

# PROBLEM
# Calculate a bonus score without changing the caller's original integer.
#
# INPUTS: An original score and a bonus.
# OUTPUTS: The original score and returned score.
#
# PLAN (PSEUDOCODE)
# 1. Pass the original score to a function.
# 2. Reassign the local parameter.
# 3. Return and compare the new value.

def add_bonus(score, bonus):
    """Return a new score without changing the caller's integer."""
    score = score + bonus
    print(f"Inside function: {score}")
    return score


if __name__ == "__main__":
    score = 70
    adjusted_score = add_bonus(score, 5)
    print(f"Original: {score}")
    print(f"Adjusted: {adjusted_score}")

# DESK CHECK
# Inside function: 75; original: 70; adjusted: 75.
#
# TRY IT: Call add_bonus twice with different bonuses.
# DISCUSS: What happens to the returned result if the caller does not store or use it?
