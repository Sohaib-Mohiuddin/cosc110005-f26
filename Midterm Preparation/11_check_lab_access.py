"""Midterm preparation 11: Check lab access."""

# WEEK 4 FOCUS: Boolean expressions using and, or, and not.
#
# WORK IN YOUR OWN FILE
# Copy this starter code into a new .py file in your own practice folder.
# Complete the TODO sections in your copy and test it with the cases below.
# The starter is intentionally incomplete; it does not yet solve the problem.
#
# PROBLEM
# Decide whether a visitor may enter a practice lab under the example rules.
#
# REQUIREMENTS
# 1. Access requires completed safety training, no suspension, and EITHER
#    a booking OR an accompanying tutor.
# 2. Create can_enter using a single expression with and, or, not, and parentheses.
# 3. Display the Boolean can_enter and "Access approved" or "Access denied".
# 4. Also display needs_training, the opposite of training_complete.
# 5. Use the supplied Boolean inputs directly; no text input is needed.
#
# CHECK YOUR WORK
# Supplied values: access approved; can_enter True; needs_training False.
# Set has_tutor False as well as has_booking False: access denied.
# With training complete and no suspension, either a booking or a tutor is enough.
# Suspension always denies access, even with both booking and tutor.
# Incomplete training always denies access; needs_training becomes True.

# STARTER CODE
training_complete = True
has_booking = False
has_tutor = True
is_suspended = False

# TODO: Calculate can_enter and needs_training from the supplied values.

# TODO: Display the Boolean results and the appropriate access message.
