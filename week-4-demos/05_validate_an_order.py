"""Demo 5: Validate before calculating."""

# PROBLEM
# Price an order of one to ten workshop kits. A recognized code removes $2 per kit.
#
# INPUTS: Quantity text and an optional STUDENT code.
# OUTPUTS: Order total or an error.
#
# PLAN (PSEUDOCODE)
# 1. Read quantity and normalize the code.
# 2. Check integer conversion, quantity range, and code.
# 3. Calculate only after all checks pass.

quantity_text = input("Kit quantity (1-10): ")
code = input("Discount code (STUDENT or blank): ").strip().upper()
try:
    quantity = int(quantity_text)
except ValueError:
    print("Quantity must be a whole number.")
else:
    if not 1 <= quantity <= 10:
        print("Choose between 1 and 10 kits.")
    elif code != "" and code != "STUDENT":
        print("Unknown discount code.")
    else:
        unit_price = 15
        if code == "STUDENT":
            unit_price = unit_price - 2
        print(f"Order total: ${quantity * unit_price:.2f}")

# DESK CHECK
# 2 kits with student cost $26.00; 2 with no code cost $30.00.
#
# TRY IT: Try 0 kits, eleven, and an unknown code.
# DISCUSS: Which validation message appears when both inputs are invalid?
