"""Demo 6: Find minimum and maximum values as input arrives."""

# PROBLEM
# Track shortest and longest study sessions without storing every entry.
#
# INPUTS: Nonnegative integer minutes, or done to finish.
# OUTPUTS: The minimum and maximum, or a no-data message.
#
# PLAN (PSEUDOCODE)
# 1. Start with no minimum or maximum.
# 2. Read and validate entries until done.
# 3. Initialize both extremes from the first valid entry, then update them.

shortest = None
longest = None
while True:
    entry = input("Session minutes (or done): ").strip().lower()
    if entry == "done":
        break
    try:
        minutes = int(entry)
    except ValueError:
        print("Enter a whole number or done.")
        continue
    if minutes < 0:
        print("Minutes cannot be negative.")
        continue
    if shortest is None:
        shortest = minutes
        longest = minutes
    else:
        if minutes < shortest:
            shortest = minutes
        if minutes > longest:
            longest = minutes
if shortest is None:
    print("No sessions entered.")
else:
    print(f"Shortest: {shortest} minutes; longest: {longest} minutes")

# DESK CHECK
# 30, 10, 45, done gives shortest 10 and longest 45.
# done alone gives no sessions; 0, done gives both extremes as 0.
#
# TRY IT: Try one entry, equal entries, and invalid entries before the first valid one.
# DISCUSS: Why would initializing shortest to zero give a misleading result?
