"""Demo 4: Process a collection using an accumulator and a counter."""

# PROBLEM
# Calculate the average of a student's equally weighted quiz scores.
# Assume the list contains valid numeric scores from 0 to 100.
#
# INPUT: A list of quiz scores. The list may be empty.
# OUTPUT: The average score, or a message if there are no scores.
#
# PLAN (PSEUDOCODE)
# 1. Set the running total and score count to zero.
# 2. For each score in the list:
#      Add the score to the running total.
#      Increase the score count by one.
# 3. If at least one score was counted:
#      Divide the total by the count and display the average.
# 4. Otherwise, report that no average can be calculated.

quiz_scores = [75, 80, 90, 85]
total_score = 0
score_count = 0

# A for loop visits each item in the list once, in order.
# total_score is an accumulator: it keeps a running total.
# score_count is a counter: it records how many items we have processed.
for score in quiz_scores:
    total_score = total_score + score
    score_count = score_count + 1
    print(f"After quiz {score_count}: running total = {total_score}")

# Check the count before dividing so an empty list does not cause an error.
if score_count > 0:
    average_score = total_score / score_count
    print(f"Average quiz score: {average_score:.2f}")
else:
    print("No quiz scores are available. There is no average yet.")

# DESK CHECK
# Score processed:   75   80   90   85
# Running total:     75  155  245  330
# Score count:        1    2    3    4
# Expected result: 330 / 4 = 82.50.
#
# TRY IT: Add a score of 100 and predict the new average.
# Then try [90] and [] to check the one-score and no-score cases.
# DISCUSS: Why do we calculate the final average after the loop?
