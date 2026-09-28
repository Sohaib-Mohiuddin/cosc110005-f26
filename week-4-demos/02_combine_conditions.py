"""Demo 2: Combine Boolean conditions."""

# PROBLEM
# Decide whether a student may borrow a classroom camera under example rules.
#
# INPUTS: Training status, reservation status, and overdue item count.
# OUTPUTS: Eligibility and an explanation.
#
# PLAN (PSEUDOCODE)
# 1. Require training and a reservation.
# 2. Require no overdue items.
# 3. Choose a message from the combined result.

training_complete = True
has_reservation = True
overdue_items = 0  # Assume a nonnegative integer.

can_borrow = training_complete and has_reservation and overdue_items == 0
if can_borrow:
    print("Camera checkout approved.")
else:
    print("Complete training, reserve a camera, and return overdue items.")

needs_preparation = not training_complete or not has_reservation
print(f"Preparation still needed: {needs_preparation}")

# DESK CHECK
# True and True and True gives approval. Preparation still needed is False.
#
# TRY IT: Change one input at a time and predict both outputs.
# DISCUSS: How does replacing and with or change the eligibility rule?
