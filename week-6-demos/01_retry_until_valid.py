"""Demo 1: Repeat validation until input is acceptable."""

# PROBLEM
# Ask for a workshop group size until it is a whole number from 1 to 6.
#
# INPUTS: Keyboard entries.
# OUTPUTS: The first accepted group size.
#
# PLAN (PSEUDOCODE)
# 1. Repeat the prompt.
# 2. Reject conversion and range errors.
# 3. Stop when a valid size is received.

while True:
    entry = input("Group size (1-6): ")
    try:
        group_size = int(entry)
    except ValueError:
        print("Enter a whole number.")
        continue  # Start the next repetition immediately.
    if 1 <= group_size <= 6:
        break  # Exit the loop only after validation succeeds.
    print("Choose a size from 1 to 6.")
print(f"Group size accepted: {group_size}")

# DESK CHECK
# Entries two, 0, 7, 4 produce three errors, then accept 4.
#
# TRY IT: Try the boundary values 1 and 6.
# DISCUSS: What condition makes this while True loop stop?
