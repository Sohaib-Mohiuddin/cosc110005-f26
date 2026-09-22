"""Demo 1: Choose types and meaningful variable names."""

# PROBLEM
# Describe a student workshop using text, whole numbers, decimals, and a Boolean.
#
# INPUTS: Workshop details stored in variables.
# OUTPUTS: Values and their Python types.
#
# PLAN (PSEUDOCODE)
# 1. Store each detail using a suitable type.
# 2. Display each value and its type.
# 3. Update the participant count.

workshop_name = "Python practice"
participant_count = 18
session_hours = 1.5
registration_open = True

print(workshop_name, type(workshop_name))
print(participant_count, type(participant_count))
print(session_hours, type(session_hours))
print(registration_open, type(registration_open))

# Assignment replaces the previous value; it is not an algebraic equation.
participant_count = participant_count + 2
print(f"Updated participant count: {participant_count}")

# DESK CHECK
# The types are str, int, float, and bool. The updated count is 20.
#
# TRY IT: Change session_hours to 2 and then 2.0. Compare the types.
# DISCUSS: Why should a student ID such as "001234" be stored as text?
