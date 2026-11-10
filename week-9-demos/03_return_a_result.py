"""Demo 3: Return a value for the caller to use."""

# PROBLEM
# Calculate a rectangular study area, then reuse the result in a second calculation.
#
# INPUTS: Nonnegative length and width.
# OUTPUTS: Area and example setup cost.
#
# PLAN (PSEUDOCODE)
# 1. Define a function that returns length times width.
# 2. Store the returned value.
# 3. Use the value in output and another calculation.

def rectangle_area(length, width):
    """Return area; assume nonnegative numeric dimensions."""
    return length * width


if __name__ == "__main__":
    area = rectangle_area(4, 10)
    setup_cost = area * 5
    print(f"Area: {area} square metres")
    print(f"Example setup cost: ${setup_cost:.2f}")

# DESK CHECK
# 4 * 3 returns 12; the caller calculates 12 * 5 = $60.00.
#
# TRY IT: Try dimensions 0 and 3, then 2.5 and 4.
# DISCUSS: Why is returning a number more reusable than printing it inside the function?
