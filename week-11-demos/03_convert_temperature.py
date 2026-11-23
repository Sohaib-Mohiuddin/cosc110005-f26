"""Demo 3: Keep calculations separate from GUI callbacks."""

# PROBLEM
# Convert a whole-number Celsius temperature to Fahrenheit.
#
# INPUTS: Integer Celsius text from -100 to 100.
# OUTPUTS: A Fahrenheit result or validation feedback.
#
# PLAN (PSEUDOCODE)
# 1. Define a calculation function independent of Tkinter.
# 2. Convert and validate entry text in a callback.
# 3. Calculate and update the result label.

import tkinter as tk
from tkinter import ttk


def celsius_to_fahrenheit(celsius):
    """Return Fahrenheit for a numeric Celsius temperature."""
    return celsius * 9 / 5 + 32


def main():
    root = tk.Tk()
    root.title('Keep calculations separate from GUI callbacks')
    frame = ttk.Frame(root, padding=20)
    frame.grid(row=0, column=0, sticky="nsew")
    entered = tk.StringVar()
    result = tk.StringVar(value="Enter a whole number, such as 20.")

    def convert():
        try:
            celsius = int(entered.get())
        except ValueError:
            result.set("Celsius must be a whole number.")
            return
        if not -100 <= celsius <= 100:
            result.set("Choose a temperature from -100 to 100 Celsius.")
            return
        result.set(f"Fahrenheit: {celsius_to_fahrenheit(celsius):.1f}")

    ttk.Label(frame, text="Celsius (-100 to 100, whole number):").grid(row=0, column=0)
    entry = ttk.Entry(frame, textvariable=entered)
    entry.grid(row=1, column=0, pady=5)
    ttk.Button(frame, text="Convert", command=convert).grid(row=2, column=0)
    ttk.Label(frame, textvariable=result).grid(row=3, column=0, pady=10)
    root.bind("<Return>", lambda event: convert())
    entry.focus_set()
    root.mainloop()


if __name__ == "__main__":
    main()

# DESK CHECK
# 0 C gives 32.0 F; 100 C gives 212.0 F; -40 C gives -40.0 F; text gives an error.
#
# TRY IT: Try blank, 3.5, -101, and 101. Correct an invalid entry and resubmit.
# DISCUSS: How could the calculation function be tested without a window?
