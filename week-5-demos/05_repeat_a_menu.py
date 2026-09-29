"""Demo 5: Keep a menu running until exit."""

# PROBLEM
# Let a student request study suggestions repeatedly.
#
# INPUTS: Menu choices 1, 2, or 0.
# OUTPUTS: A suggestion, error, or goodbye message.
#
# PLAN (PSEUDOCODE)
# 1. Display choices.
# 2. Handle the selection.
# 3. Repeat until the user chooses 0.

choice = ""
while choice != "0":
    print("\n1. Review notes\n2. Practise code\n0. Exit")
    choice = input("Choice: ").strip()
    if choice == "1":
        print("Summarize one concept in your own words.")
    elif choice == "2":
        print("Trace a loop before running it.")
    elif choice == "0":
        print("Goodbye!")
    else:
        print("Choose 1, 2, or 0.")

# DESK CHECK
# 1, 9, 2, 0 gives two suggestions, one error, and then exits.
#
# TRY IT: Add a third study activity and update the displayed menu.
# DISCUSS: Why can menu choices stay as strings?
