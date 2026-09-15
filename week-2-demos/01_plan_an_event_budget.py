"""Demo 1: Plan a solution before writing code, then follow a sequence."""

# PROBLEM
# A college club needs to estimate the cost of a pizza event.
# Assume everyone shares the cost equally and tax is already included.
#
# INPUTS: Number of pizzas, price per pizza, drink cost, and student count.
# PROCESS: Calculate the pizza cost, add drinks, then divide among students.
# OUTPUTS: The total event cost and the estimated cost per student.
#
# PLAN (PSEUDOCODE)
# 1. Store the event details.
# 2. Multiply the number of pizzas by the price of one pizza.
# 3. Add the drink cost to the pizza cost.
# 4. Divide the total cost by the number of students.
# 5. Display the results.
#
# PRECONDITION: The student count must be greater than zero so we can divide.

# Step 1: Named variables make the inputs easy to find and change.
pizza_count = 6
price_per_pizza = 14.00
drink_cost = 24.00
student_count = 12

# Steps 2-4: Order matters. Each calculation uses an earlier result.
pizza_cost = pizza_count * price_per_pizza
total_cost = pizza_cost + drink_cost
cost_per_student = total_cost / student_count

# Step 5: An f-string inserts values into text; .2f shows two decimal places.
print("College club event budget")
print(f"Total event cost: ${total_cost:.2f}")
print(f"Estimated cost per student: ${cost_per_student:.2f}")

# DESK CHECK: Work through the plan by hand before running the program.
# 6 * 14.00 = 84.00; 84.00 + 24.00 = 108.00; 108.00 / 12 = 9.00.
# Expected output: a total of $108.00 and $9.00 per student.
#
# TRY IT: Change student_count to 18. Predict the new cost per student.
# DISCUSS: How could the plan handle a student count of zero?
