"""Demo 2: Convert input text into numbers."""

# PROBLEM
# Estimate the number of pages read during a study session.
# For this first input demo, enter valid, nonnegative whole numbers.
#
# INPUTS: Pages read per minute and minutes spent reading.
# OUTPUTS: Total pages read.
#
# PLAN (PSEUDOCODE)
# 1. Read both values as text.
# 2. Convert the text to integers.
# 3. Multiply and display the result.

pages_text = input("Pages per minute (whole number): ")
minutes_text = input("Minutes reading (whole number): ")

# input() always returns a string, even when the user types digits.
pages_per_minute = int(pages_text)
minutes = int(minutes_text)
total_pages = pages_per_minute * minutes
print(f"Estimated pages read: {total_pages}")

# DESK CHECK
# Enter 2 and 15: 2 * 15 = 30 pages. Enter 0 and 15: 0 pages.
#
# TRY IT: Enter "two" and inspect the ValueError. Week 4 will handle this case.
# DISCUSS: How do "2" + "15" and int("2") + int("15") differ?
