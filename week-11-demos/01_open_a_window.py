"""Demo 1: Introduce widgets and the event loop."""

# PROBLEM
# Open a course welcome window and respond to a button click.
#
# INPUTS: A click on the Start button.
# OUTPUTS: A changed status label.
#
# PLAN (PSEUDOCODE)
# 1. Create a window and its widgets.
# 2. Connect the button to a callback function.
# 3. Start the event loop and wait for user actions.

import tkinter as tk
from tkinter import ttk


def main():
    root = tk.Tk()
    root.title('Introduce widgets and the event loop')
    frame = ttk.Frame(root, padding=20)
    frame.grid(row=0, column=0, sticky="nsew")
    status = tk.StringVar(value="Ready to begin.")

    def start_activity():
        status.set("Activity started: trace a function call.")

    ttk.Label(frame, text="Welcome to Python interfaces").grid(row=0, column=0, pady=5)
    ttk.Label(frame, textvariable=status).grid(row=1, column=0, pady=5)
    # Pass the function itself. start_activity() would call it immediately.
    button = ttk.Button(frame, text="Start", command=start_activity)
    button.grid(row=2, column=0, pady=5)
    button.focus_set()
    # mainloop below handles clicks and redraws until the window closes.
    root.mainloop()


if __name__ == "__main__":
    main()

# DESK CHECK
# Initially: Ready to begin. Clicking Start changes the status to the activity message.
#
# TRY IT: Change the message, then use Tab and Space to activate the button.
# DISCUSS: Why does a GUI use an event loop instead of repeated input() calls?
