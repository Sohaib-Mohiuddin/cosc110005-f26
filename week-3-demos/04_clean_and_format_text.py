"""Demo 4: Clean and format strings."""

# PROBLEM
# Prepare a workshop registration name and course code for display.
#
# INPUTS: Text containing extra spaces and inconsistent capitalization.
# OUTPUTS: Cleaned text and its length.
#
# PLAN (PSEUDOCODE)
# 1. Remove surrounding whitespace.
# 2. Normalize the course code.
# 3. Display a formatted label.

entered_name = "  Alex Chen  "
entered_course = " cosc1100-05 "
student_name = entered_name.strip()
course_code = entered_course.strip().upper()

# Strings are immutable: these methods return new strings.
print(f"Original name: [{entered_name}]")
print(f"Name badge: {student_name} | {course_code}")
print(f"Name length: {len(student_name)} characters")

# DESK CHECK
# The cleaned name is Alex Chen (9 characters); the code is COSC1100-05.
#
# TRY IT: Add spaces inside the name. Does strip() remove them?
# DISCUSS: Why should we avoid automatically changing capitalization in a person's name?
