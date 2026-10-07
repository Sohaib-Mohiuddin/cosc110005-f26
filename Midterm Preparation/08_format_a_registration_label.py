"""Midterm preparation 08: Format a registration label."""

# WEEK 3 FOCUS: String cleaning, case conversion, length, and f-strings.
#
# WORK IN YOUR OWN FILE
# Copy this starter code into a new .py file in your own practice folder.
# Complete the TODO sections in your copy and test it with the cases below.
# The starter is intentionally incomplete; it does not yet solve the problem.
#
# PROBLEM
# Clean a student's name and course code to make a readable registration label.
#
# REQUIREMENTS
# 1. Ask for a name and a course code. Assume both contain non-whitespace text.
# 2. Remove surrounding whitespace from both inputs with strip().
# 3. Preserve the name's capitalization and any spaces inside the name.
# 4. Convert the cleaned course code to uppercase.
# 5. Display "Name: <name> | Course: <course>" and the cleaned name's length.
# 6. Also display the original name inside square brackets to show the difference.
# 7. Save the cleaned values in new variables; retain the original input strings.
#
# CHECK YOUR WORK
# Name "  Sam Lee  ", code " cosc1100-05 ":
# Name: Sam Lee | Course: COSC1100-05; cleaned name length 7.
# Name "Jo  Wu" has length 6: its two internal spaces must remain.
# Explain in a comment why strip() alone does not change the original variable.

# STARTER CODE
entered_name = input("Student name: ")
entered_course = input("Course code: ")

# TODO: Create student_name and course_code using the required string methods.

# TODO: Display the original input, formatted label, and cleaned name length.
