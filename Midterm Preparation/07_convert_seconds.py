"""Midterm preparation 07: Convert seconds."""

# WEEK 3 FOCUS: Integer division, remainder, and arithmetic order.
#
# WORK IN YOUR OWN FILE
# Copy this starter code into a new .py file in your own practice folder.
# Complete the TODO sections in your copy and test it with the cases below.
# The starter is intentionally incomplete; it does not yet solve the problem.
#
# PROBLEM
# Convert a whole-number duration in seconds into hours, minutes, and seconds.
#
# REQUIREMENTS
# 1. Ask for a nonnegative whole number of seconds; assume valid input.
# 2. Use // and % to calculate complete hours, remaining minutes, and seconds.
# 3. Minutes and seconds in the result must each be from 0 through 59.
# 4. Display all three parts with clear labels. Zero-padding is not required.
# 5. Reconstruct the original duration from the three parts and print it.
# 6. Do not import a time library; practise arithmetic with the constants below.
#
# CHECK YOUR WORK
# 3665 -> 1 hour, 1 minute, 5 seconds; reconstructed total 3665.
# 59 -> 0 hours, 0 minutes, 59 seconds; 60 -> 0 hours, 1 minute, 0 seconds.
# 3600 -> 1 hour, 0 minutes, 0 seconds; 0 -> all three parts are zero.

# STARTER CODE
SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 3600
total_seconds = int(input("Total seconds: "))

# TODO: Calculate hours, minutes, and seconds using // and %.

# TODO: Print the three parts, then calculate and display reconstructed_seconds.
