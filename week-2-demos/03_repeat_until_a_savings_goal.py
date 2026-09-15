"""Demo 3: Repeat steps with a while loop until a goal is reached."""

# PROBLEM
# Count how many weekly deposits are needed to afford a $120 textbook.
# Use whole dollars and assume the price and weekly deposit stay constant.
#
# INPUTS: Savings goal, current savings, and weekly deposit.
# OUTPUTS: A weekly progress trace and the number of weeks needed.
#
# PLAN (PSEUDOCODE)
# 1. Start the week counter at zero.
# 2. If the goal is already reached, report zero weeks.
# 3. Otherwise, if the deposit is not positive, explain why we cannot proceed.
# 4. Otherwise, while savings are below the goal:
#      Add one weekly deposit to savings.
#      Increase the week counter by one.
#      Display the week's savings.
# 5. Display the number of weeks needed and the final savings.

savings_goal = 120
current_savings = 0
weekly_deposit = 25
weeks = 0

if current_savings >= savings_goal:
    print("The savings goal is already reached. Weeks needed: 0")
elif weekly_deposit <= 0:
    # A zero or negative deposit would prevent the loop from reaching its goal.
    print("Use a positive weekly deposit to make progress toward the goal.")
else:
    # A while loop checks its condition before every repetition.
    # The deposit increases savings each time, so this loop will eventually stop.
    while current_savings < savings_goal:
        current_savings = current_savings + weekly_deposit
        weeks = weeks + 1
        print(f"Week {weeks}: ${current_savings} saved")

    # This code runs after the loop because it is outside the loop's indentation.
    print(f"Weeks needed: {weeks}")
    print(f"Final savings: ${current_savings}")

# DESK CHECK
# Week:       0   1   2   3    4    5
# Savings:    0  25  50  75  100  125
# Expected result: 5 weeks. Reaching OR exceeding the goal is enough.
#
# TRY IT: Set weekly_deposit to 40, then 0. Explain each result.
# DISCUSS: Why would checking current_savings != savings_goal be a mistake?
