"""Companion module for demo 6: reusable study-duration calculations."""


def split_minutes(total_minutes):
    """Return (hours, minutes); assume a nonnegative integer input."""
    return total_minutes // 60, total_minutes % 60


if __name__ == "__main__":
    # This example runs directly, but not when another script imports us.
    print(f"Helper example: {split_minutes(90)}")
