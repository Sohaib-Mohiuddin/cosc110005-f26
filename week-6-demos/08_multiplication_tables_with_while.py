"""Demo 8: Reset an inner while-loop counter and total for each table."""

# PROBLEM
# Print the first four products in each multiplication table from 1 to 3.
# Also print the sum of the products in each individual table.
#
# INPUTS: Positive integer table and multiplier limits, set below.
# OUTPUTS: Three multiplication tables, each followed by its own total.
#
# PLAN (PSEUDOCODE)
# 1. Start with table 1.
# 2. For each table, reset the multiplier to 1 and the table total to 0.
# 3. Calculate, print, and add each product; advance the multiplier.
# 4. Print the completed table total, then advance to the next table.

last_table = 10
last_multiplier = 10
table = 1

while table <= last_table:
    print(f"Table {table}")

    # These assignments run once per TABLE, before its inner loop starts.
    # Resetting multiplier lets every table start at 1.
    # Resetting table_total keeps earlier tables' products out of this total.
    multiplier = 1
    table_total = 0

    while multiplier <= last_multiplier:
        # table stays fixed until this entire inner loop has finished.
        product = table * multiplier
        print(f"{table} x {multiplier} = {product}")
        table_total = table_total + product
        multiplier = multiplier + 1  # Advance the INNER loop on every repetition.

    # The inner loop has ended: multiplier is now last_multiplier + 1.
    print(f"Table total: {table_total}")
    print()  # A blank line separates completed tables.
    table = table + 1  # Advance the OUTER loop only after finishing one table.

# DESK CHECK
# table    multiplier values    products       table_total
# 1        1, 2, 3, 4           1, 2, 3, 4     10
# 2        1, 2, 3, 4           2, 4, 6, 8     20
# 3        1, 2, 3, 4           3, 6, 9, 12    30
# There are 3 * 4 = 12 product lines and 3 table totals.
# After table 1, multiplier is 5; the reset makes it 1 again for table 2.
#
# EXPECTED OUTPUT FOR THE FIRST TABLE
# Table 1
# 1 x 1 = 1
# 1 x 2 = 2
# 1 x 3 = 3
# 1 x 4 = 4
# Table total: 10
#
# TRY IT: Set last_table to 2 and last_multiplier to 3. Totals should be 6 and 12.
# DISCUSS: If multiplier = 1 were placed before the outer loop, why would later
# tables have no product lines? Trace multiplier after the first table finishes.
# DISCUSS: What happens to the totals if table_total = 0 moves before the outer loop?
# DISCUSS: Why would removing either counter update cause an infinite loop?
