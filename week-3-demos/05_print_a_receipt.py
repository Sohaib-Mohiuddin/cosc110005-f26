"""Demo 5: Calculate and format a small receipt."""

# PROBLEM
# Calculate a notebook purchase using integer cents to represent money.
# The discount is a fixed amount for this classroom example.
#
# INPUTS: Quantity, unit price in cents, and discount in cents.
# OUTPUTS: Subtotal and amount due.
#
# PLAN (PSEUDOCODE)
# 1. Multiply quantity by unit price.
# 2. Subtract the discount.
# 3. Convert cents to dollars for display.

quantity = 3
unit_price_cents = 425
discount_cents = 100  # Assume 0 <= discount <= subtotal.
subtotal_cents = quantity * unit_price_cents
amount_due_cents = subtotal_cents - discount_cents

print("Campus supplies")
print(f"Notebooks: {quantity} @ ${unit_price_cents / 100:.2f}")
print(f"Subtotal: ${subtotal_cents / 100:.2f}")
print(f"Discount: ${discount_cents / 100:.2f}")
print(f"Amount due: ${amount_due_cents / 100:.2f}")

# DESK CHECK
# 3 * 425 = 1275 cents; subtract 100 to get 1175 cents ($11.75).
#
# TRY IT: Change quantity to 5 and predict the receipt.
# DISCUSS: Why keep calculations in cents and format dollars only for output?
