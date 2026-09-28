"""Demo 4: Separate conversion errors from range errors."""

# PROBLEM
# Accept one proposed workshop attendance count.
#
# INPUTS: Keyboard text for a count between 1 and 30.
# OUTPUTS: An accepted count or a helpful error.
#
# PLAN (PSEUDOCODE)
# 1. Read and strip the text.
# 2. Try to convert it to an integer.
# 3. If conversion succeeds, check the allowed range.

entered_count = input("Attendance (1-30): ").strip()
try:
    attendance = int(entered_count)
except ValueError:
    print("Enter a whole number, such as 12.")
else:
    if 1 <= attendance <= 30:
        print(f"Attendance recorded: {attendance}")
    else:
        print("Attendance must be from 1 to 30.")

# DESK CHECK
# 12 is accepted; 0 and 31 fail the range check; twelve fails conversion.
#
# TRY IT: Try an empty entry, 3.5, and spaces around 12.
# DISCUSS: Why is successful conversion not enough to accept the value?
