"""Demo 1: Define a function and call it more than once."""

# PROBLEM
# Display the same course heading at the beginning of two activities.
#
# INPUTS: No function arguments.
# OUTPUTS: A reusable heading and two activity labels.
#
# PLAN (PSEUDOCODE)
# 1. Define the heading function.
# 2. Call it for activity one.
# 3. Call it again for activity two.

def show_heading():
    """Print the shared heading; return None implicitly."""
    print("COSC1100-05")
    print("Python practice")


if __name__ == "__main__":
    # The guard runs this demonstration only when the file is executed.
    show_heading()
    print("Activity 1: trace a loop\n")
    show_heading()
    print("Activity 2: write a function")

# DESK CHECK
# The two-line heading appears twice, once before each activity.
#
# TRY IT: Change the heading in one place and run both calls again.
# DISCUSS: How is defining a function different from executing it?
