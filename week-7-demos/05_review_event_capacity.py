"""Demo 5: Integrate validation, selection, and a running total."""

# PROBLEM
# Accept group bookings until the user enters 0, without exceeding ten seats.
#
# INPUTS: Whole-number group sizes; 0 finishes.
# OUTPUTS: Booking decisions and remaining seats.
#
# PLAN (PSEUDOCODE)
# 1. Start with ten seats.
# 2. Repeat until 0, rejecting invalid groups.
# 3. Subtract only accepted group sizes.

seats_remaining = 10
while True:
    try:
        group_size = int(input("Group size (0 to finish): "))
    except ValueError:
        print("Enter a whole number.")
        continue
    if group_size == 0:
        break
    if group_size < 0:
        print("Group size cannot be negative.")
    elif group_size > seats_remaining:
        print("Not enough seats for that group.")
    else:
        seats_remaining = seats_remaining - group_size
        print(f"Booked {group_size}; seats remaining: {seats_remaining}")
print(f"Final seats remaining: {seats_remaining}")

# DESK CHECK
# 3, 8, 7, 0 accepts 3, rejects 8, accepts 7, and ends with 0 seats.
#
# TRY IT: Start with 0, then try a separate run with text and a negative group size.
# DISCUSS: What fact about seats_remaining should stay true throughout the program?
