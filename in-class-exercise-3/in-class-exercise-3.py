# COSC 1100 - Selection: Planning to Validate
# Instructor demonstration using four student attributes.
# Group members: Replace this line with your group's names when submitting.
# These validation rules are classroom assumptions, not college policy.
# Simple plan: input -> validate using selection -> output if all fields pass.

# Start by assuming the record is valid; any failed check changes this to False.
is_valid = True

# INPUT: Read the four attributes as text and remove surrounding whitespace.
student_name = input("Enter student name (1-100 characters): ").strip()
student_id = input("Enter student ID (exactly 9 digits, no spaces): ").strip()
course_count_text = input("Enter courses enrolled in (whole number, 1-8): ").strip()
exercise_mark_text = input("Enter exercise mark (whole number, 0-100, no % sign): ").strip()

# PROCESS: Check the name for missing input, length, and permitted characters.
# For this example, allow letters, spaces, hyphens, apostrophes, and periods.
# Removing allowed separators lets isalpha() check that letters remain.
name_letters = student_name.replace(" ", "").replace("-", "")
name_letters = name_letters.replace("'", "").replace("\u2019", "").replace(".", "")
if student_name == "":
    print("Name error: Enter a name; spaces alone are not accepted.")
    is_valid = False
elif len(student_name) > 100:
    print("Name error: Use no more than 100 characters.")
    is_valid = False
elif not name_letters.isalpha():
    print("Name error: Include a letter and use only letters, spaces, hyphens, apostrophes, or periods.")
    is_valid = False

# Check the ID for missing input, exact length, and digits from 0 to 9 only.
# Keep the ID as text so that leading zeros are preserved.
if student_id == "":
    print("ID error: Enter your student ID.")
    is_valid = False
elif len(student_id) != 9:
    print("ID error: Enter exactly 9 digits.")
    is_valid = False
elif not (student_id.isascii() and student_id.isdigit()):
    print("ID error: Use only digits 0-9, with no letters, spaces, or punctuation.")
    is_valid = False

# Check course-count presence and format before attempting numeric conversion.
# A one-digit limit also prevents unnecessarily long numeric input.
if course_count_text == "":
    print("Course count error: Enter the number of courses.")
    is_valid = False
elif not (course_count_text.isascii() and course_count_text.isdigit()):
    print("Course count error: Enter a whole number using only digits 0-9.")
    is_valid = False
elif len(course_count_text) > 1:
    print("Course count error: Enter one digit from 1 to 8.")
    is_valid = False
else:
    course_count = int(course_count_text)
    # Once conversion is safe, check both ends of the permitted range.
    if course_count < 1 or course_count > 8:
        print("Course count error: The number must be from 1 to 8 inclusive.")
        is_valid = False

# Check mark presence, format, and length before converting it to an integer.
if exercise_mark_text == "":
    print("Mark error: Enter an exercise mark.")
    is_valid = False
elif not (exercise_mark_text.isascii() and exercise_mark_text.isdigit()):
    print("Mark error: Enter a whole number using only digits 0-9, without a % sign.")
    is_valid = False
elif len(exercise_mark_text) > 3:
    print("Mark error: Use at most 3 digits for a mark from 0 to 100.")
    is_valid = False
else:
    exercise_mark = int(exercise_mark_text)
    # A numeric value can still be invalid if it lies outside the allowed range.
    if exercise_mark < 0 or exercise_mark > 100:
        print("Mark error: The mark must be from 0 to 100 inclusive.")
        is_valid = False

# OUTPUT: Display the completed record only when every field passed validation.
if is_valid:
    print("\nValidated student information")
    print("Student name:", student_name)
    print("Student ID:", student_id)
    print("Courses enrolled in:", course_count)
    print("Exercise mark:", exercise_mark)
else:
    print("\nStudent information was not accepted. Correct the errors and run again.")
