"""Demo 3: Nest a decision when it depends on another."""

# PROBLEM
# Choose an example campus event ticket price.
#
# INPUTS: Student status and whether a student has a valid student card.
# OUTPUTS: Ticket price in dollars.
#
# PLAN (PSEUDOCODE)
# 1. Check whether the visitor is a student.
# 2. For a student, check the card.
# 3. Display the selected price.

is_student = True
has_student_card = False
if is_student:
    if has_student_card:
        ticket_price = 5
    else:
        ticket_price = 8
else:
    ticket_price = 12
print(f"Ticket price: ${ticket_price:.2f}")

# DESK CHECK
# A student without a card pays $8.00. A nonstudent pays $12.00.
#
# TRY IT: Trace all four combinations of the two Boolean inputs.
# DISCUSS: Why is the card check inside the student branch?
