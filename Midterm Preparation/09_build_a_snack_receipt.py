"""Midterm preparation 09: Build a snack receipt."""

# WEEK 3 FOCUS: Integer cents, arithmetic, and monetary formatting.
#
# WORK IN YOUR OWN FILE
# Copy this starter code into a new .py file in your own practice folder.
# Complete the TODO sections in your copy and test it with the cases below.
# The starter is intentionally incomplete; it does not yet solve the problem.
#
# PROBLEM
# Create a receipt for granola bars and juice boxes with a fixed coupon discount.
#
# REQUIREMENTS
# 1. Use the supplied quantities and prices, with all calculations in integer cents.
# 2. Calculate each line total, the subtotal, and the amount due after the coupon.
# 3. Display both quantities and line totals, subtotal, coupon, and amount due.
# 4. Convert cents to dollars only for display and show two decimal places.
# 5. Assume nonnegative integer quantities and 0 <= coupon <= subtotal.
#    Prices already include tax; do not calculate additional tax.
# 6. Add a comment explaining why the coupon is subtracted only once per order.
#
# CHECK YOUR WORK
# Supplied order: bars $5.00, juice $5.25, subtotal $10.25,
# coupon $1.25, amount due $9.00.
# Coupon 0: amount due $10.25. Coupon 1025: amount due $0.00.
# For an empty order, use zero quantities AND a zero coupon.

# STARTER CODE
bar_quantity = 2
bar_price_cents = 250
juice_quantity = 3
juice_price_cents = 175
coupon_cents = 125

# TODO: Calculate each line total, subtotal_cents, and amount_due_cents.

print("Study break snacks")
# TODO: Complete the receipt with labelled quantities and monetary amounts.
