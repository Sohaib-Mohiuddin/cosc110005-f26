"""Demo 3: Use division, remainder, and precedence."""

# PROBLEM
# Pack students into full shuttle trips and identify the remaining passengers.
#
# INPUTS: Student count and positive shuttle capacity.
# OUTPUTS: Full trips, remaining students, and an arithmetic comparison.
#
# PLAN (PSEUDOCODE)
# 1. Divide using // to count full trips.
# 2. Use % to find the remainder.
# 3. Compare expressions with and without parentheses.

student_count = 29
shuttle_capacity = 8  # Must be greater than zero.
full_trips = student_count // shuttle_capacity
remaining_students = student_count % shuttle_capacity

print(f"Full trips: {full_trips}")
print(f"Students needing another trip: {remaining_students}")
print(f"Ordinary division: {student_count / shuttle_capacity}")
print(f"2 + 3 * 4 = {2 + 3 * 4}")
print(f"(2 + 3) * 4 = {(2 + 3) * 4}")

# DESK CHECK
# 29 // 8 = 3; 29 % 8 = 5; 29 / 8 = 3.625. Expressions give 14 and 20.
#
# TRY IT: Try 32 students, then 0 students. Predict the remainders.
# DISCUSS: Why are full trips alone insufficient to transport all 29 students?
