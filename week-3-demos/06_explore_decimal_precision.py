"""Demo 6: Distinguish stored values from display formatting."""

# PROBLEM
# Compare decimal-looking floating-point values and integer cents.
# Many decimal fractions cannot be represented exactly as binary floats.
#
# INPUTS: The values 0.1 and 0.2, and their integer-cent equivalents.
# OUTPUTS: Raw values, equality results, and formatted output.
#
# PLAN (PSEUDOCODE)
# 1. Add two floating-point values.
# 2. Compare the result with 0.3 and format it.
# 3. Repeat using whole cents.

total = 0.1 + 0.2
print(f"Stored result: {total!r}")
print(f"Exactly equal to 0.3: {total == 0.3}")
print(f"Displayed with two places: {total:.2f}")
# Formatting produces text; it does not change the stored number.
print(f"Stored result after formatting: {total!r}")

total_cents = 10 + 20
print(f"Integer cents: {total_cents}")
print(f"Exactly equal to 30 cents: {total_cents == 30}")
print(f"Dollar display: ${total_cents / 100:.2f}")

# DESK CHECK
# The float sum prints 0.30000000000000004 and equality is False.
# The formatted value is 0.30, while integer cents equal 30 exactly.
#
# TRY IT: Try 0.5 + 0.25. Does every floating-point sum have the same visible issue?
# DISCUSS: Why does formatting to two decimal places not make the stored value exact?
