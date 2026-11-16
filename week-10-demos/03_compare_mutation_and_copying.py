"""Demo 3: Distinguish aliases, mutation, and copies."""

# PROBLEM
# Compare a function that changes a score list with one that returns a new list.
#
# INPUTS: Lists of numeric scores and a bonus.
# OUTPUTS: Original, aliased, and copied results.
#
# PLAN (PSEUDOCODE)
# 1. Demonstrate two names referring to one list.
# 2. Mutate that list through a function.
# 3. Copy a fresh list before updating it.

def add_bonus_in_place(scores, bonus):
    """Change the supplied list; return None implicitly."""
    for index in range(len(scores)):
        scores[index] = scores[index] + bonus


def scores_with_bonus(scores, bonus):
    """Return a modified copy of a flat numeric list."""
    result = scores.copy()
    add_bonus_in_place(result, bonus)
    return result


if __name__ == "__main__":
    original = [60, 70]
    alias = original
    add_bonus_in_place(alias, 5)
    print(f"Original after alias mutation: {original}")
    fresh_scores = [60, 70]
    adjusted = scores_with_bonus(fresh_scores, 5)
    print(f"Fresh original: {fresh_scores}; returned copy: {adjusted}")

# DESK CHECK
# Aliased original becomes [65, 75]. Fresh original stays [60, 70].
#
# TRY IT: Check alias is original and adjusted is fresh_scores.
# DISCUSS: Why does rebinding an integer parameter differ from changing a list element?
