"""Demo 2: Use selection to choose one path through an algorithm."""

# PROBLEM
# Suggest a study activity based on the number of minutes available.
# These are example rules for this demonstration.
#
# INPUT: Available time, expressed as a whole number of minutes.
# OUTPUT: One suggested activity, or a message about an invalid time.
#
# PLAN (PSEUDOCODE)
# 1. Read the available time from a variable.
# 2. If the time is negative, report an invalid value.
# 3. Otherwise, if there are at least 60 minutes, suggest a practice quiz.
# 4. Otherwise, if there are at least 30 minutes, suggest practice problems.
# 5. Otherwise, if there are at least 15 minutes, suggest reviewing notes.
# 6. Otherwise, suggest planning the next study session.
# 7. Display the chosen suggestion.

minutes_available = 45

# An if/elif/else chain chooses only the first matching branch.
# Check the largest time threshold first. Checking 15 first would also
# match someone with 60 minutes and give them the wrong suggestion.
if minutes_available < 0:
    suggestion = "Please use a time of zero minutes or more."
elif minutes_available >= 60:
    suggestion = "Complete a practice quiz and review your answers."
elif minutes_available >= 30:
    suggestion = "Work through a few practice problems."
elif minutes_available >= 15:
    suggestion = "Review your class notes."
else:
    suggestion = "Write down a goal for your next study session."

print(f"Available time: {minutes_available} minutes")
print(suggestion)

# DESK CHECK: With 45 minutes, the negative and >= 60 checks are false.
# The >= 30 check is true, so the program suggests practice problems.
#
# TRY IT: Predict the output for -1, 0, 14, 15, 29, 30, 59, and 60 minutes.
# These values test the boundaries where the chosen branch changes.
