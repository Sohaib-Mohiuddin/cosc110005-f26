"""Demo 2: Change the size of a list."""

# PROBLEM
# Update a supply list as items are added and packed.
#
# INPUTS: An initial list of supplies.
# OUTPUTS: The revised list and the removed item.
#
# PLAN (PSEUDOCODE)
# 1. Append one item and insert another.
# 2. Remove a known item by value.
# 3. Pop the last item and display the result.

supplies = ["pen", "notebook"]
supplies.append("calculator")
supplies.insert(1, "pencil")
print(f"After additions: {supplies}")
if "pen" in supplies:
    supplies.remove("pen")
if len(supplies) > 0:
    packed_item = supplies.pop()
    print(f"Packed: {packed_item}")
print(f"Still to pack: {supplies}")

# DESK CHECK
# Additions: pen, pencil, notebook, calculator. Remaining: pencil, notebook.
#
# TRY IT: Start with an empty list and trace the same operations.
# DISCUSS: What is the difference between remove(value) and pop(index)?
