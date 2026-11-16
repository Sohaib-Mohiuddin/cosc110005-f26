"""Demo 2: Package linear search as a reusable function."""

# PROBLEM
# Find the first matching item and return its index.
#
# INPUTS: A list and a target value.
# OUTPUTS: An index or None.
#
# PLAN (PSEUDOCODE)
# 1. Compare elements in order.
# 2. Return immediately at the first match.
# 3. Return None after exhausting the list.

def find_index(items, target):
    """Return the first matching index, or None if absent."""
    for index in range(len(items)):
        if items[index] == target:
            return index
    return None


if __name__ == "__main__":
    supplies = ["pen", "notebook", "pen"]
    position = find_index(supplies, "notebookk")
    # Index 0 is a match, even though bool(0) is False.
    if position is None:
        print("Item not found.")
    else:
        print(f"Found at index {position}.")

# DESK CHECK
# Searching for pen returns 0, the index of the first match.
#
# TRY IT: Search for notebook and calculator, then search an empty list.
# DISCUSS: Why would if position: mishandle a match at index 0?
