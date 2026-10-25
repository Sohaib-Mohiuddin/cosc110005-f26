"""Demo 5: Traverse rows and columns."""

# PROBLEM
# Summarize two quizzes for each of three students using a rectangular table.
#
# INPUTS: A list of rows; each row contains two valid quiz scores.
# OUTPUTS: Each student's total.
#
# PLAN (PSEUDOCODE)
# 1. Visit each row by index.
# 2. Visit the scores within that row.
# 3. Display the row total.

quiz_scores = [[70, 80], [90, 85], [60, 75]]
for row_index in range(len(quiz_scores)):
    row_total = 0  # Reset once per student, not once for the entire table.
    for column_index in range(len(quiz_scores[row_index])):
        row_total = row_total + quiz_scores[row_index][column_index]
    print(f"Student {row_index + 1}: total {row_total}")

# DESK CHECK
# Student totals are 150, 175, and 135.
#
# TRY IT: Add a fourth row and predict its total.
# DISCUSS: Which index identifies the student and which identifies the quiz?
