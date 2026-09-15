"""Demo 5: Use linear search to find an item one comparison at a time."""

# PROBLEM
# Check whether a backpack contains an item needed for class.
#
# INPUTS: A list of packed items and the name of the required item.
# OUTPUTS: Whether the item was found and the number of items checked.
#
# PLAN (PSEUDOCODE)
# 1. Start with found set to false and the comparison count set to zero.
# 2. For each packed item:
#      Increase the comparison count.
#      Compare the packed item with the required item.
#      If they match, set found to true and stop searching.
# 3. Report whether the item was found.
# 4. Display the comparison count.

packed_items = ["notebook", "calculator", "pen", "USB drive"]
required_item = "calculator"
found = False
items_checked = 0

# This is called linear search because we check items one by one.
# We write out the search steps to see how the algorithm works.
for item in packed_items:
    items_checked = items_checked + 1
    print(f"Checking item {items_checked}: {item}")

    # == compares values; = assigns a value to a variable.
    # This comparison is exact: "Calculator" differs from "calculator".
    if item == required_item:
        found = True
        # break exits the loop immediately. Later items do not need checking.
        break

if found:
    print(f"Ready for class: {required_item} is packed.")
else:
    print(f"Remember to pack: {required_item}.")

print(f"Items checked: {items_checked}")

# DESK CHECK: "notebook" does not match; "calculator" does match.
# Expected result: the item is found after 2 comparisons.
#
# TRY IT: Search for "notebook", "USB drive", and "laptop". Predict the counts.
# Then use an empty list. It should report a missing item and 0 checks.
# DISCUSS: With 100 items, what are the fewest and most checks we might need?
