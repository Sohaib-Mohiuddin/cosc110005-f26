"""Demo 5: Combine labelled fields in a form."""

# PROBLEM
# Preview a workshop registration using a name and fixed session choice.
# This classroom form stores nothing after it closes.
#
# INPUTS: A nonblank name and a session selected from a read-only dropdown.
# OUTPUTS: A registration preview.
#
# PLAN (PSEUDOCODE)
# 1. Create a grid of labels and inputs.
# 2. Validate the name when Preview is clicked.
# 3. Display both selections together.

import tkinter as tk
from tkinter import ttk


def main():
    root = tk.Tk()
    root.title('Combine labelled fields in a form')
    frame = ttk.Frame(root, padding=20)
    frame.grid(row=0, column=0, sticky="nsew")
    name = tk.StringVar()
    session = tk.StringVar(value="Morning")
    result = tk.StringVar(value="Complete the form to preview.")

    def preview():
        cleaned_name = name.get().strip()
        if cleaned_name == "":
            result.set("Enter a display name before previewing.")
            name_entry.focus_set()
            return
        result.set(f"Preview: {cleaned_name} | {session.get()} session")

    ttk.Label(frame, text="Display name:").grid(row=0, column=0, sticky="w", padx=5)
    name_entry = ttk.Entry(frame, textvariable=name)
    name_entry.grid(row=0, column=1, pady=5)
    ttk.Label(frame, text="Session:").grid(row=1, column=0, sticky="w", padx=5)
    ttk.Combobox(frame, textvariable=session, values=["Morning", "Afternoon"],
                 state="readonly").grid(row=1, column=1, pady=5)
    ttk.Button(frame, text="Preview registration", command=preview).grid(
        row=2, column=0, columnspan=2, pady=10)
    ttk.Label(frame, textvariable=result).grid(row=3, column=0, columnspan=2)
    root.bind("<Return>", lambda event: preview())
    name_entry.focus_set()
    root.mainloop()


if __name__ == "__main__":
    main()

# DESK CHECK
# Alex with Afternoon selected produces Preview: Alex | Afternoon session.
#
# TRY IT: Navigate using Tab and submit with Enter; try a blank name.
# DISCUSS: When does a fixed set of choices make validation easier?
