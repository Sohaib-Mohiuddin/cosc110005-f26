"""Demo 5: Split a program into focused functions."""

# PROBLEM
# Read a valid group size and calculate the cost of $8 workshop tickets.
#
# INPUTS: A whole-number group size from 1 to 10.
# OUTPUTS: The booking total.
#
# PLAN (PSEUDOCODE)
# 1. Read and validate input in one function.
# 2. Calculate the total in a separate function.
# 3. Coordinate both from main.

def read_group_size():
    """Retry until a whole number from 1 to 10 is entered."""
    while True:
        try:
            size = int(input("Group size (1-10): "))
        except ValueError:
            print("Enter a whole number.")
            continue
        
        if 1 <= size <= 10:
            return size
        print("Choose a size from 1 to 10.")


def calculate_total(group_size, ticket_price):
    """Return the cost; assume validated size and nonnegative price."""
    return group_size * ticket_price


def main():
    size = read_group_size()
    total = calculate_total(size, 8)
    print(f"Booking total: ${total:.2f}")


if __name__ == "__main__":
    main()

# DESK CHECK
# A size of 3 costs $24.00. Invalid entries are retried before calculation.
#
# TRY IT: Change the ticket price in main and test both size boundaries.
# DISCUSS: Which function could be reused by a graphical interface?
