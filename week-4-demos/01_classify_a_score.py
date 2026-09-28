"""Demo 1: Order branches and check boundaries."""

# PROBLEM
# Classify a practice score using example feedback bands, not official course grades.
#
# INPUTS: A numeric score.
# OUTPUTS: One feedback message or a range error.
#
# PLAN (PSEUDOCODE)
# 1. Reject scores outside 0 through 100.
# 2. Check the highest band first.
# 3. Display one message.

score = 80
if score < 0 or score > 100:
    feedback = "Score must be between 0 and 100."
elif score >= 80:
    feedback = "Ready for a challenge."
elif score >= 60:
    feedback = "Keep practising."
else:
    feedback = "Review the worked examples."
print(feedback)

# DESK CHECK
# 80 selects the highest band; 79 selects Keep practising.
#
# TRY IT: Check -1, 0, 59, 60, 79, 80, 100, and 101.
# DISCUSS: What happens if the >= 60 branch comes before >= 80?
