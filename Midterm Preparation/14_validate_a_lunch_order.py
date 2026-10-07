"""Midterm preparation 14: Validate a lunch order."""

# WEEK 4 FOCUS: Input validation, normalization, and guarded calculations.
#
# WORK IN YOUR OWN FILE
# Copy this starter code into a new .py file in your own practice folder.
# Complete the TODO sections in your copy and test it with the cases below.
# The starter is intentionally incomplete; it does not yet solve the problem.
#
# PROBLEM
# Price an order of lunch boxes only after both quantity and discount code are valid.
#
# REQUIREMENTS
# 1. Read quantity text and a code; strip the code and convert it to uppercase.
# 2. Quantity must convert to an integer from 1 through 8.
# 3. Allowed codes are blank (no discount) or CLASS (a $2 discount PER BOX).
# 4. Each lunch box normally costs $9.00. Prices already include tax.
# 5. Validate in this order: integer conversion, quantity range, allowed code.
# 6. Print only the first validation error, or a labelled total to two decimals.
#    Invalid input must not produce an order total. Prompt only once per field.
#
# CHECK YOUR WORK
# Quantity 3 and code " class " -> $21.00; 3 and blank -> $27.00.
# 1 with CLASS -> $7.00; 8 with CLASS -> $56.00.
# "two" fails conversion; 0 and 9 fail the range check; SAVE fails the code check.
# 0 with SAVE must report the quantity error before considering the code.

# STARTER CODE
UNIT_PRICE = 9
DISCOUNT_PER_BOX = 2
quantity_text = input("Lunch boxes (1-8): ")
entered_code = input("Code (CLASS or blank): ")

# TODO: Normalize the discount code.

try:
    # TODO: Convert quantity_text to quantity.
    pass
except ValueError:
    # TODO: Print a helpful whole-number error.
    pass
else:
    # TODO: Check the range, then the code; calculate only if both are valid.
    pass
