"""Demo 4: Stop input with a sentinel value."""

# PROBLEM
# Record practice scores until the user enters done.
#
# INPUTS: Integer scores from 0 to 100, or done.
# OUTPUTS: Average of valid scores, or a no-scores message.
#
# PLAN (PSEUDOCODE)
# 1. Initialize a total and count.
# 2. Read until done, validating each score.
# 3. Calculate an average only when the count is positive.

total = 0
count = 0
entry = input("Score (0-100), or done: ").strip().lower()
while entry != "done":
    try:
        score = int(entry)
    except ValueError:
        print("Enter a whole-number score or done.")
    else:
        if 0 <= score <= 100:
            total = total + score
            count = count + 1
        else:
            print("Scores must be from 0 to 100.")
    # Read again on both valid and invalid paths.
    entry = input("Score (0-100), or done: ").strip().lower()
if count > 0:
    print(f"Average: {total / count:.2f}")
else:
    print("No scores entered.")

# DESK CHECK
# 80, 90, done gives 85.00. done as the first entry gives no average.
#
# TRY IT: Enter bad, -1, 100, and done. Only 100 should be counted.
# DISCUSS: Why is done checked before conversion?
