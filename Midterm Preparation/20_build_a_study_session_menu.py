"""Midterm preparation 20: Build a study session menu."""

# WEEK 5 FOCUS: Repeated menus, state, selection, and accumulation.
#
# WORK IN YOUR OWN FILE
# Copy this starter code into a new .py file in your own practice folder.
# Complete the TODO sections in your copy and test it with the cases below.
# The starter is intentionally incomplete; it does not yet solve the problem.
#
# PROBLEM
# Build a small menu that records completed study sessions during one program run.
#
# REQUIREMENTS
# 1. Repeatedly display: 1. Record 15-minute review; 2. Record 30-minute coding;
#    3. Show summary; 0. Exit. Read the choice as stripped text.
# 2. Choice 1 adds 15 minutes and one session; choice 2 adds 30 minutes and one session.
# 3. Choice 3 displays total sessions and total minutes without changing either.
# 4. Choice 0 displays the final totals and "Goodbye!", then ends the loop.
# 5. Any other choice, including blank input, displays an error and repeats the menu.
# 6. Initialize totals once before the while loop; retain them between choices.
# 7. Do not convert menu choices to integers. No functions or imports are required.
#
# CHECK YOUR WORK
# 1, 2, 3, 9, 0: summary and final totals both show 2 sessions and 45 minutes;
# 9 produces one error and does not change the totals.
# 3, 0: both summaries show 0 sessions and 0 minutes.
# 1, 1, 0: final totals 2 sessions and 30 minutes.
# " 2 ", blank, 0: final totals 1 session and 30 minutes, with one error.

# STARTER CODE
choice = ""
total_sessions = 0
total_minutes = 0

# TODO: Write a while loop that continues until choice is "0".
# Display the menu and read a new choice inside the loop.
# TODO: Use if/elif/else to handle all four choices and invalid input.
# TODO: Update totals only for choices 1 and 2; display them for choices 3 and 0.
