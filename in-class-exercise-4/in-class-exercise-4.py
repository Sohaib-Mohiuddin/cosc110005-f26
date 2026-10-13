# COSC 1100 - Class Exercise 4: Iteration
# Purpose: Record hot-dog sales, then display totals and percentages.
# Group members: Add your group's names here when submitting.
#
# PLANNING
# ========
# Problem: John needs to record orders for three types of hot dogs, maintain
# running sales totals, and display counts and percentages when he finishes.
# Use an outer while loop for the menu because the number of orders is unknown.
# Use an inner while loop to retry an invalid quantity for the selected type.
# This demonstration uses no break or continue statements.
#
# INPUT
# -----
# 1. choice: Menu option entered as text.
#    "1" = Traditional, "2" = Veggie Dog, "3" = Curry Hot Dog,
#    "4" = Tally and exit. No quantity is requested for option 4.
# 2. quantity_text: Number sold in the current order, entered as text.
#    Convert to integer quantity only after validating the text.
# 3. Remove surrounding whitespace from both inputs before checking them.
#
# Validation and assumptions:
# - Menu input must be exactly 1, 2, 3, or 4 after trimming.
# - Quantity must contain one or more ordinary digits 0-9.
# - Zero is allowed and adds no sales; leading zeros are allowed (003 means 3).
# - Reject blank quantities, negatives, signs, decimals, letters, internal
#   spaces, commas, underscores, and other non-digit characters.
# - If Python cannot convert an unusually long digit string, show an error
#   and ask for a shorter quantity.
# - Invalid input never changes sales totals.
# - A quantity of 4 means four hot dogs; only MENU option 4 ends data entry.
#
# OUTPUT
# ------
# 1. Repeated menu and prompts for menu choices and quantities.
# 2. Specific error messages for invalid menu input or quantities.
# 3. Confirmation after each accepted quantity is recorded.
# 4. Final number sold for Traditional, Veggie Dog, and Curry Hot Dog.
# 5. Each type's percentage of all hot dogs sold, to two decimal places.
# 6. Grand total and every type tied for the highest sales count.
# 7. If there are no sales, show zero counts and 0.00% as a reporting
#    convention, plus a message explaining that no type is most popular.
# 8. Goodbye message before the program ends.
#
# PROCESS
# -------
# 1. Initialize traditional_total, veggie_total, and curry_total to 0 ONCE,
#    before the menu loop. These variables accumulate quantities across orders.
# 2. Set finished to False and repeat the menu while not finished.
# 3. For option 4, set finished to True to stop the outer loop.
# 4. For options 1-3, reset quantity_valid to False for this order.
#    Repeat the quantity prompt until format checking and conversion succeed.
# 5. Add the accepted quantity to exactly one accumulator, then show the menu
#    again. Add it outside the inner loop so retries cannot double-count sales.
# 6. For an invalid menu choice, show an error and repeat the menu.
# 7. After the menu loop, calculate:
#       total_sold = traditional_total + veggie_total + curry_total
# 8. If total_sold > 0, calculate each percentage:
#       type_percent = type_total / total_sold * 100
#    Otherwise, set all three displayed percentages to 0.0. Never divide by 0.
# 9. Display the final counts, percentages, and grand total.
# 10. If sales exist, find the highest count and display every matching type.
#     Use separate checks so ties are included. Otherwise, report no sales.
# 11. Display Goodbye and end. Rounded percentages may not add to exactly 100%.
#
# PSEUDOCODE
# ----------
# START
#   SET traditional_total, veggie_total, curry_total TO 0
#   SET finished TO False
#   WHILE NOT finished
#       DISPLAY menu
#       INPUT choice and trim surrounding whitespace
#       IF choice = "4" THEN
#           SET finished TO True
#       ELSE IF choice = "1" OR choice = "2" OR choice = "3" THEN
#           SET quantity_valid TO False
#           WHILE NOT quantity_valid
#               INPUT quantity_text and trim surrounding whitespace
#               IF quantity_text contains one or more digits 0-9 only THEN
#                   ATTEMPT to convert quantity_text to integer quantity
#                   IF conversion succeeds THEN
#                       SET quantity_valid TO True
#                   ELSE
#                       DISPLAY conversion error
#                   END IF
#               ELSE
#                   DISPLAY quantity format error
#               END IF
#           END WHILE
#           IF choice = "1" THEN
#               ADD quantity TO traditional_total
#           ELSE IF choice = "2" THEN
#               ADD quantity TO veggie_total
#           ELSE
#               ADD quantity TO curry_total
#           END IF
#           DISPLAY entry confirmation
#       ELSE
#           DISPLAY menu error
#       END IF
#   END WHILE
#   SET total_sold TO traditional_total + veggie_total + curry_total
#   IF total_sold > 0 THEN
#       CALCULATE each type_percent AS type_total / total_sold * 100
#   ELSE
#       SET all three percentages TO 0.0
#   END IF
#   DISPLAY each type's count and percentage, and total_sold
#   IF total_sold > 0 THEN
#       SET highest_total TO largest of the three type totals
#       IF traditional_total = highest_total THEN
#           DISPLAY Traditional as a most popular type
#       END IF
#       IF veggie_total = highest_total THEN
#           DISPLAY Veggie Dog as a most popular type
#       END IF
#       IF curry_total = highest_total THEN
#           DISPLAY Curry Hot Dog as a most popular type
#       END IF
#   ELSE
#       DISPLAY no-sales message
#   END IF
#   DISPLAY Goodbye
# END
#
# DESKCHECK
# ---------
# Trace the accumulators after each action. T = Traditional, V = Veggie,
# C = Curry. Rejected input leaves all three totals unchanged.
#
# Step | Menu / quantity entered | T | V | C | Expected action
# -----+-------------------------+---+---+---+-----------------------------
#   0  | Program starts          | 0 | 0 | 0 | Display menu
#   1  | Menu 9                  | 0 | 0 | 0 | Error; repeat menu
#   2  | Menu 1, quantity 3      | 3 | 0 | 0 | Add 3 Traditional
#   3  | Menu 2, quantity -2     | 3 | 0 | 0 | Error; retry same quantity
#   4  | Retry quantity 2        | 3 | 2 | 0 | Add 2 Veggie
#   5  | Menu 1, quantity 1      | 4 | 2 | 0 | Add 1; preserve earlier 3
#   6  | Menu 3, quantity 4      | 4 | 2 | 4 | Add 4 Curry; keep running
#   7  | Menu 4                  | 4 | 2 | 4 | Set finished True; tally
#
# total_sold = 4 + 2 + 4 = 10
# traditional_percent = 4 / 10 * 100 = 40.00%
# veggie_percent      = 2 / 10 * 100 = 20.00%
# curry_percent       = 4 / 10 * 100 = 40.00%
# Most popular types: Traditional and Curry Hot Dog (tie at 4 each).
#
# Additional checks (each starts a fresh program run):
# - Menu 4 immediately: all totals 0, all percentages 0.00%, no-sales message.
# - Menu 2, quantity 0, then menu 4: accept 0; same no-sales result.
# - Menu 1, quantities blank, 2.5, abc, then 3: first three attempts rejected;
#   add exactly 3 Traditional once, then return to the menu.
# - Menu " 2 ", quantity " 003 ", then menu 4: trim input; Veggie total 3,
#   Veggie percentage 100.00%; other types 0.00%.
# - Record 1 of each type, then menu 4: total 3; each displays 33.33%; all tie.
#
# END OF PLANNING - IMPLEMENTATION FOLLOWS
# ======================================

# Initialize the accumulators once, before the menu loop.
traditional_total = 0
veggie_total = 0
curry_total = 0
finished = False

# OUTER LOOP: Keep accepting orders until the user selects option 4.
while not finished:
    # INPUT: Display the menu on every pass and read the choice as text.
    print("\nJOHN'S HOT-DOG STAND")
    print("1. Traditional")
    print("2. Veggie Dog")
    print("3. Curry Hot Dog")
    print("4. Tally and exit")
    choice = input("Enter a menu option (1-4): ").strip()

    # Option 4 ends data entry; it must not ask for a quantity.
    if choice == "4":
        finished = True
    elif choice == "1" or choice == "2" or choice == "3":
        # Reset validation for this order, without resetting any sales totals.
        quantity_valid = False

        # INNER LOOP: Retry the quantity for the same type until it is valid.
        while not quantity_valid:
            quantity_text = input("Enter number sold (whole number, 0 or more): ").strip()

            # Require at least one ordinary digit; reject signs and decimals.
            if quantity_text.isascii() and quantity_text.isdigit():
                # Conversion occurs only after the format check succeeds.
                # Python may reject unusually long digit strings with ValueError.
                try:
                    quantity = int(quantity_text)
                    quantity_valid = True
                except ValueError:
                    print("Quantity error: Too many digits. Enter a shorter whole number.")
            else:
                print("Quantity error: Use digits 0-9 only; enter 0 or more.")

        # PROCESS: Add the validated quantity to exactly one accumulator.
        # This block is outside the inner loop, so invalid attempts add nothing.
        if choice == "1":
            traditional_total = traditional_total + quantity
        elif choice == "2":
            veggie_total = veggie_total + quantity
        else:
            curry_total = curry_total + quantity

        # Confirm the entry, then let the outer loop display the menu again.
        print("Recorded", quantity, "hot dog(s).")
    else:
        # Invalid menu input changes no totals; the outer loop prompts again.
        print("Menu error: Enter 1, 2, 3, or 4.")

# PROCESS: Calculate the final tally only after the menu loop finishes.
total_sold = traditional_total + veggie_total + curry_total

# Guard against division by zero when no hot dogs have been sold.
if total_sold > 0:
    traditional_percent = traditional_total / total_sold * 100
    veggie_percent = veggie_total / total_sold * 100
    curry_percent = curry_total / total_sold * 100
else:
    traditional_percent = 0.0
    veggie_percent = 0.0
    curry_percent = 0.0

# OUTPUT: Display each type's count and share of all hot dogs sold.
print("\nFINAL SALES TALLY")
print(f"{'Hot-dog type':<18}{'Number sold':>12}{'Percent':>12}")
print(f"{'Traditional':<18}{traditional_total:>12}{traditional_percent:>11.2f}%")
print(f"{'Veggie Dog':<18}{veggie_total:>12}{veggie_percent:>11.2f}%")
print(f"{'Curry Hot Dog':<18}{curry_total:>12}{curry_percent:>11.2f}%")
print("Total hot dogs sold:", total_sold)

# Identify every type with the highest total, including any ties.
if total_sold > 0:
    highest_total = max(traditional_total, veggie_total, curry_total)
    print("Most popular type(s):")
    # Separate if statements ensure that tied types are all displayed.
    if traditional_total == highest_total:
        print("Traditional")
    if veggie_total == highest_total:
        print("Veggie Dog")
    if curry_total == highest_total:
        print("Curry Hot Dog")
else:
    print("No sales were recorded; there is no most popular type.")

print("Goodbye!")
