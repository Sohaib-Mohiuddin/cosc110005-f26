"""Demo 2: Pass values into parameters."""

# PROBLEM
# Print a personalized study reminder using the same function.
#
# INPUTS: A student name and a positive number of minutes for each call.
# OUTPUTS: Two reminders.
#
# PLAN (PSEUDOCODE)
# 1. Define parameters for name and minutes.
# 2. Use the parameters in a message.
# 3. Call with different arguments.

def show_reminder(student_name, minutes):
    """Display a reminder; assume minutes is a positive integer."""
    print(f"{student_name}, schedule {minutes} minutes of practice.")


if __name__ == "__main__":
    show_reminder("Alex", 20)
    show_reminder("Sam", 35)

# DESK CHECK
# Alex receives a 20-minute reminder; Sam receives a 35-minute reminder.
#
# TRY IT: Call show_reminder(minutes=15, student_name="Jordan").
# DISCUSS: Which names are parameters, and which values are arguments?
