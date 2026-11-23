"""Demo 2: Read entry text and display feedback."""

# PROBLEM
# Greet a student by a nonblank display name.
#
# INPUTS: Text entered in a labelled field.
# OUTPUTS: A greeting or a useful validation message.
#
# PLAN (PSEUDOCODE)
# 1. Create an entry and output label.
# 2. Trim and validate on button click or Enter.
# 3. Update the output label.

import tkinter as tk
from tkinter import ttk


def main():
    root = tk.Tk()
    root.title('Read entry text and display feedback')
    frame = ttk.Frame(root, padding=20)
    frame.grid(row=0, column=0, sticky="nsew")
    name = tk.StringVar()
    feedback = tk.StringVar(value="Enter your display name.")

    def greet():
        cleaned_name = name.get().strip()
        if cleaned_name == "":
            feedback.set("Please enter a name.")
            entry.focus_set()
        else:
            feedback.set(f"Welcome, {cleaned_name}!")

    ttk.Label(frame, text="Display name:").grid(row=0, column=0, sticky="w")
    entry = ttk.Entry(frame, textvariable=name, width=30)
    entry.grid(row=1, column=0, pady=5)
    ttk.Button(frame, text="Create greeting", command=greet).grid(row=2, column=0)
    ttk.Label(frame, textvariable=feedback).grid(row=3, column=0, pady=10)
    # A key binding supplies an event argument; a button command does not.
    root.bind("<Return>", lambda event: greet())
    entry.focus_set()
    root.mainloop()


if __name__ == "__main__":
    main()

# DESK CHECK
# Spaces give Please enter a name. Entering " Alex " gives Welcome, Alex!
#
# TRY IT: Submit using Enter, then try the button with an empty field.
# DISCUSS: Why should feedback explain how to correct the input?
