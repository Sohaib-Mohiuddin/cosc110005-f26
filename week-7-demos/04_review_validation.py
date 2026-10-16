"""Demo 4: Review validation with a limited number of attempts."""

# PROBLEM
# Allow up to three attempts to enter a nonblank display name of at most 20 characters.
#
# INPUTS: Display name text.
# OUTPUTS: An accepted name or an exhausted-attempts message.
#
# PLAN (PSEUDOCODE)
# 1. Repeat at most three times.
# 2. Trim and check each entry.
# 3. Stop on success; report failure if no entry was accepted.

accepted = False
for attempt in range(1, 4):
    name = input(f"Display name, attempt {attempt}/3: ").strip()
    if 1 <= len(name) <= 20:
        accepted = True
        break
    print("Use 1 to 20 characters after trimming spaces.")
if accepted:
    print(f"Welcome, {name}!")
else:
    print("No valid name entered. Run again to retry.")

# DESK CHECK
# Blank, 21 characters, Alex succeeds on attempt 3; three blanks fail.
#
# TRY IT: Try exactly 20 characters and spaces around a short name.
# DISCUSS: Why keep a separate accepted flag?
