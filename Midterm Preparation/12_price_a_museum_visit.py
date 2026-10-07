"""Midterm preparation 12: Price a museum visit."""

# WEEK 4 FOCUS: Nested decisions and dependent conditions.
#
# WORK IN YOUR OWN FILE
# Copy this starter code into a new .py file in your own practice folder.
# Complete the TODO sections in your copy and test it with the cases below.
# The starter is intentionally incomplete; it does not yet solve the problem.
#
# PROBLEM
# Choose a museum admission price using the example membership rules below.
#
# REQUIREMENTS
# 1. Members with a valid membership card pay $4.00.
# 2. Members without a valid card pay $7.00.
# 3. Nonmembers aged 12 or younger pay $6.00; other nonmembers pay $11.00.
# 4. Use an outer decision for membership and nested decisions for card or age.
# 5. For members, age does not affect the price. For nonmembers, card does not.
# 6. Assume age is a nonnegative integer. Print one price to two decimal places.
#
# CHECK YOUR WORK
# Supplied member without a card, age 10 -> $7.00.
# Member with a card, any valid age -> $4.00.
# Nonmember age 12 -> $6.00; nonmember age 13 -> $11.00.
# Change a nonmember's card flag and verify that their price does not change.

# STARTER CODE
is_member = True
has_membership_card = False
age = 10

if is_member:
    # TODO: Add a nested card decision and assign admission_price.
    pass
else:
    # TODO: Add a nested age decision and assign admission_price.
    pass

# TODO: Display admission_price after all branches assign it.
