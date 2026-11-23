"""Demo 4: Use radio buttons for one choice."""

# PROBLEM
# Choose one study activity and optionally request a reminder.
# This demo only previews preferences; it does not send reminders.
#
# INPUTS: One radio selection and a checkbox state.
# OUTPUTS: A summary of the chosen settings.
#
# PLAN (PSEUDOCODE)
# 1. Share one variable among radio buttons.
# 2. Use a Boolean variable for the checkbox.
# 3. Read both variables when settings are applied.

import tkinter as tk
from tkinter import ttk


def main():
    root = tk.Tk()
    root.title('Use radio buttons for one choice')
    frame = ttk.Frame(root, padding=20)
    frame.grid(row=0, column=0, sticky="nsew")
    activity = tk.StringVar(value="Practice problems")
    wants_reminder = tk.BooleanVar(value=False)
    summary = tk.StringVar(value="Choose your settings, then apply.")

    def apply_settings():
        reminder_text = "on" if wants_reminder.get() else "off"
        summary.set(f"Activity: {activity.get()} | Reminder: {reminder_text}")

    ttk.Label(frame, text="Choose one activity:").grid(row=0, column=0, sticky="w")
    for row, label in enumerate(["Review notes", "Practice problems", "Practice quiz"], start=1):
        ttk.Radiobutton(frame, text=label, variable=activity, value=label).grid(
            row=row, column=0, sticky="w")
    ttk.Checkbutton(frame, text="Request a reminder", variable=wants_reminder).grid(
        row=4, column=0, sticky="w", pady=5)
    ttk.Button(frame, text="Apply settings", command=apply_settings).grid(row=5, column=0)
    ttk.Label(frame, textvariable=summary).grid(row=6, column=0, pady=10)
    root.mainloop()


if __name__ == "__main__":
    main()

# DESK CHECK
# Applying the defaults shows Practice problems and Reminder: off.
#
# TRY IT: Select Practice quiz, check the reminder box, and apply again.
# DISCUSS: Why do radio buttons share a variable while the checkbox uses a separate one?
