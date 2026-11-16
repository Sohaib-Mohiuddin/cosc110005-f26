"""Assignment 1 worked solution: Square Numbers - Iteration."""

# DESCRIPTION
# Display every square number in an inclusive range supplied by the user.
# Show the whole-number root beside each square, for example: 9 (3 squared).
# This is an instructor-requested teaching example prepared with OpenAI Codex.
# Source requirements: COSC1100.Assignment1.SquareNumbers.pdf, Durham College.
# The handout's AI-use instruction requests functions and the word "banana";
# this comment records that requirement without adding it to the output.
#
# INPUTS
# - Lower bound: a whole number from 1 through 10000.
# - Upper bound: a whole number from the accepted lower bound through 10000.
# - An Enter key press before the program finishes.
#
# PROCESSING AND OUTPUTS
# - Retry the affected input when conversion or range validation fails.
# - After both bounds are valid, generate squares using root * root.
# - Print a results banner and each square within the inclusive bounds.
# - Explain when the valid range contains no square numbers.
#
# PLAN (PSEUDOCODE)
# MAIN
#   Display the opening banner.
#   Call READ LOWER BOUND and store its result.
#   Call READ UPPER BOUND using the accepted lower bound; store its result.
#   Call DISPLAY SQUARE NUMBERS using both accepted bounds.
#   Wait for Enter before finishing.
#
# READ LOWER BOUND
#   Repeat:
#     Prompt for the lower bound and try to convert the entry to an integer.
#     If conversion fails, explain that a whole number is required and retry.
#     If the value is between 1 and 10000 inclusive, return it.
#     Otherwise, explain the allowed range and retry.
#
# READ UPPER BOUND
#   Repeat:
#     Prompt for the upper bound and try to convert the entry to an integer.
#     If conversion fails, explain that a whole number is required and retry.
#     If lower bound <= value <= 10000, return it.
#     Otherwise, explain the allowed range and retry this bound only.
#
# DISPLAY SQUARE NUMBERS
#   Display a results banner containing the accepted bounds.
#   Set root to 1, square number to root * root, and found square to false.
#   While square number <= upper bound:
#     If square number >= lower bound:
#       Display the square number and its root; set found square to true.
#     Add 1 to root, then recalculate square number as root * root.
#   If no square was displayed, print a helpful message.
#
# DESK CHECKS
# - 4..120: 4, 9, 16, 25, 36, 49, 64, 81, 100 (nine results).
# - 5..10: only 9; 10..15: no squares; 16..16: only 16.
# - 1..10000: 100 results, from 1 (1 squared) to 10000 (100 squared).
# See worked_solution.md for sample runs, a trace table, and a test plan.

MIN_BOUND = 1
MAX_BOUND = 10000
BANNER_WIDTH = 72


def display_banner(title):
    """Display a centred title between two rows of asterisks."""
    print("*" * BANNER_WIDTH)
    print(title.center(BANNER_WIDTH))
    print("*" * BANNER_WIDTH)


def read_lower_bound():
    """Retry until a whole number from 1 through 10000 is entered."""
    while True:
        try:
            lower_bound = int(input("Please enter the lower bound: "))
        except ValueError:
            print("Invalid input: Please enter a whole number.\n")
            continue

        if MIN_BOUND <= lower_bound <= MAX_BOUND:
            return lower_bound

        print("Invalid input: Please enter a number between "
              f"{MIN_BOUND} and {MAX_BOUND}.\n")


def read_upper_bound(lower_bound):
    """Retry until a whole number from lower_bound through 10000 is entered."""
    while True:
        try:
            upper_bound = int(input("Please enter the upper bound: "))
        except ValueError:
            print("Invalid input: Please enter a whole number.\n")
            continue

        if lower_bound <= upper_bound <= MAX_BOUND:
            return upper_bound

        print("Invalid input: Please enter a number between "
              f"{lower_bound} and {MAX_BOUND}.\n")


def display_square_numbers(lower_bound, upper_bound):
    """Print squares and their roots; assume both bounds are already valid."""
    display_banner(f"Square Numbers Between {lower_bound} and {upper_bound}")
    root = 1
    square_number = root * root
    found_square = False

    # Generate squares in order: at most 100 roots are examined.
    while square_number <= upper_bound:
        if square_number >= lower_bound:
            print(f"{square_number} ({root} squared)")
            found_square = True

        # Update even when the square is below the lower bound.
        root += 1
        square_number = root * root

    if not found_square:
        print("No square numbers were found in this range.")


def main():
    """Coordinate input, processing, output, and the closing pause."""
    display_banner("SQUARE NUMBER FINDER")
    print()
    lower_bound = read_lower_bound()
    upper_bound = read_upper_bound(lower_bound)
    print()
    display_square_numbers(lower_bound, upper_bound)
    input("\nPress Enter to exit...")


# Run the program when this file is executed; allow functions to be imported.
if __name__ == "__main__":
    main()
