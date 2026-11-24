"""Demo 6: Bring data, decisions, loops, and functions into a GUI."""

# PROBLEM
# Plan study sessions and track progress toward a 90-minute goal.
#
# INPUTS: Session title, topic, minutes, search text, and button clicks.
# OUTPUTS: A searchable session table, topic totals, and goal progress.
#
# PLAN (PSEUDOCODE)
# 1. Start with an empty list of rows and build the interface.
# 2. When Add is clicked, validate the fields before appending a row.
# 3. When searching, build a separate list of matching row indices.
#    If requested, use selection sort to order those indices by minutes.
# 4. To complete or remove a session, use its original index in the list.
# 5. After each change, redraw the table and recalculate the plan totals.
# 6. Let Tkinter wait for the next event until the window closes.
#
# A row holds [title, topic, minutes, completed]. Closing clears the plan.
# Run with desktop Python. For Bootstrap styling, install ttkbootstrap
# into the same Python environment. Plain ttk is used if it is absent.

import tkinter as tk
from tkinter import ttk


TOPICS = ("Data and decisions", "Loops", "Lists and functions", "Interfaces")
GOAL_MINUTES = 90
MAX_MINUTES = 180
MINUTES = 2      # Column index in a session row.
COMPLETED = 3


def make_session(title, topic, minutes_text):
    """Validate an entry and return a new row without changing the plan."""
    title = title.strip()
    if not title or len(title) > 60:
        raise ValueError("Enter a session title from 1 to 60 characters.")
    if topic not in TOPICS:
        raise ValueError("Choose a study topic.")
    try:
        minutes = int(minutes_text)
    except ValueError:
        raise ValueError("Enter minutes as a whole number.") from None
    if not 1 <= minutes <= MAX_MINUTES:
        raise ValueError(f"Enter minutes from 1 to {MAX_MINUTES}.")
    return [title, topic, minutes, False]


def matching_indices(sessions, query="", shortest_first=False):
    """Search titles and topics, optionally sorting only the view indices."""
    query = query.strip().casefold()
    indices = []
    for index, (title, topic, minutes, completed) in enumerate(sessions):
        if query not in title.casefold() and query not in topic.casefold():
            continue
        indices.append(index)

    if shortest_first:
        # Selection sort. Each pass finds the shortest remaining session.
        # The original index also breaks ties in order of entry.
        for start in range(len(indices) - 1):
            smallest = start
            for candidate in range(start + 1, len(indices)):
                left = indices[candidate]
                right = indices[smallest]
                if (sessions[left][MINUTES], left) < (
                    sessions[right][MINUTES], right
                ):
                    smallest = candidate
            indices[start], indices[smallest] = indices[smallest], indices[start]
    return indices


def summarize(sessions):
    """Return planned minutes, completed minutes, and totals by topic."""
    planned = 0
    completed_minutes = 0
    for title, topic, minutes, completed in sessions:
        planned += minutes
        if completed:
            completed_minutes += minutes

    topic_totals = []
    for topic in TOPICS:
        total = 0  # Reset the accumulator for each topic.
        for row in sessions:
            if row[1] == topic:
                total += row[MINUTES]
        topic_totals.append((topic, total))
    return planned, completed_minutes, topic_totals


def attach_tooltips(root, hints):
    """Show one delayed hint at a time for mouse and keyboard users."""
    owner = None
    pending = None
    popup = None

    def dismiss():
        nonlocal owner, pending, popup
        if pending is not None:
            root.after_cancel(pending)
            pending = None
        if popup is not None:
            if popup.winfo_exists():
                popup.destroy()
            popup = None
        owner = None

    def show(widget, text):
        nonlocal pending, popup
        pending = None
        if not widget.winfo_viewable():
            return

        popup = tk.Toplevel(root)
        popup.withdraw()
        popup.overrideredirect(True)
        ttk.Label(popup, text=text, padding=(8, 5), wraplength=255,
                  relief="solid", borderwidth=1).pack()
        popup.update_idletasks()

        # Keep the hint near its control and inside the planner window.
        right = root.winfo_rootx() + root.winfo_width()
        bottom = root.winfo_rooty() + root.winfo_height()
        x = min(widget.winfo_rootx(), right - popup.winfo_reqwidth())
        y = widget.winfo_rooty() + widget.winfo_height() + 5
        if y + popup.winfo_reqheight() > bottom:
            y = widget.winfo_rooty() - popup.winfo_reqheight() - 5
        popup.geometry(f"+{x}+{y}")
        popup.deiconify()

    def schedule(event, text):
        nonlocal owner, pending
        dismiss()
        owner = event.widget
        pending = root.after(500, show, owner, text)

    def leave(event):
        if event.widget is owner:
            dismiss()

    for widget, text in hints:
        for sequence in ("<Enter>", "<FocusIn>"):
            widget.bind(sequence, lambda event, text=text: schedule(event, text),
                        add="+")
        for sequence in ("<Leave>", "<FocusOut>", "<ButtonPress>",
                         "<KeyPress>", "<Destroy>"):
            widget.bind(sequence, leave, add="+")
    root.bind("<Escape>", lambda event: dismiss(), add="+")


def build_planner(root, widgets=ttk):
    """Connect Tkinter controls to the session list and its rules."""
    themed = widgets is not ttk
    root.title("Study Session Planner")
    root.minsize(780, 530)
    root.geometry("940x610")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    sessions = []
    title_input = tk.StringVar(master=root)
    topic_input = tk.StringVar(master=root, value=TOPICS[0])
    minutes_input = tk.StringVar(master=root)
    search_input = tk.StringVar(master=root)
    shortest_first = tk.BooleanVar(master=root)
    status = tk.StringVar(master=root, value="Add a session to start your plan.")
    totals = tk.StringVar(master=root)
    by_topic = tk.StringVar(master=root)

    dashboard = widgets.Frame(root, padding=18)
    dashboard.grid(sticky="nsew")
    dashboard.columnconfigure(1, weight=1)
    dashboard.rowconfigure(1, weight=1)
    heading = widgets.Label(dashboard, text="Study Session Planner", font=("TkDefaultFont", 19, "bold"))
    heading.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

    form = widgets.LabelFrame(dashboard, text="New session", padding=12)
    form.grid(row=1, column=0, sticky="new", padx=(0, 12))
    widgets.Label(form, text="Session title").grid(row=0, column=0, sticky="w")
    title_entry = widgets.Entry(form, textvariable=title_input, width=24)
    title_entry.grid(row=1, column=0, sticky="ew", pady=(3, 10))
    widgets.Label(form, text="Topic").grid(row=2, column=0, sticky="w")
    topic_picker = widgets.Combobox(form, textvariable=topic_input,
                                    values=TOPICS, state="readonly")
    topic_picker.grid(row=3, column=0, sticky="ew", pady=(3, 10))
    widgets.Label(form, text=f"Minutes (1–{MAX_MINUTES})").grid(
        row=4, column=0, sticky="w"
    )
    minutes_entry = widgets.Spinbox(
        form, from_=1, to=MAX_MINUTES, textvariable=minutes_input, width=10
    )
    minutes_entry.grid(row=5, column=0, sticky="ew", pady=(3, 10))

    plan = widgets.LabelFrame(dashboard, text="Sessions", padding=12)
    plan.grid(row=1, column=1, sticky="nsew")
    plan.columnconfigure(1, weight=1)
    plan.rowconfigure(1, weight=1)
    widgets.Label(plan, text="Search").grid(row=0, column=0, sticky="w", padx=(0, 6))
    search_entry = widgets.Entry(plan, textvariable=search_input)
    search_entry.grid(row=0, column=1, sticky="ew")
    sort_toggle = widgets.Checkbutton(plan, text="Shortest first",
                                      variable=shortest_first)
    sort_toggle.grid(row=0, column=2, columnspan=2, sticky="e", padx=(8, 0))

    tree = widgets.Treeview(plan, columns=("title", "topic", "minutes", "status"),
                        show="headings", selectmode="browse", height=8)
    for column, label, width in [("title", "Session", 140), ("topic", "Topic", 135),
                                 ("minutes", "Min", 45), ("status", "Status", 70)]:
        tree.heading(column, text=label)
        tree.column(column, width=width, minwidth=width,
                    stretch=column in ("title", "topic"))
    tree.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=8)
    scrollbar = widgets.Scrollbar(plan, orient="vertical", command=tree.yview)
    scrollbar.grid(row=1, column=3, sticky="ns", pady=8)
    tree.configure(yscrollcommand=scrollbar.set)

    summary = widgets.LabelFrame(dashboard, text="Whole plan", padding=12)
    summary.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(12, 0))
    summary.columnconfigure(0, weight=1)
    widgets.Label(summary, textvariable=totals).grid(sticky="w")
    progress = widgets.Progressbar(summary, maximum=GOAL_MINUTES)
    progress.grid(sticky="ew", pady=6)
    widgets.Label(summary, textvariable=by_topic, wraplength=700).grid(sticky="w")
    widgets.Label(dashboard, textvariable=status, wraplength=720).grid(
        row=3, column=0, columnspan=2, sticky="w", pady=(8, 0)
    )

    def refresh(selected_index=None):
        # The table contains a view of the list. Each item ID is a model index.
        children = tree.get_children()
        if children:
            tree.delete(*children)
        visible = matching_indices(sessions, search_input.get(), shortest_first.get())
        for index in visible:
            title, topic, minutes, completed = sessions[index]
            label = "Done" if completed else "Planned"
            tree.insert("", "end", iid=str(index),
                        values=(title, topic, minutes, label))
        if selected_index in visible:
            tree.selection_set(str(selected_index))
            tree.focus(str(selected_index))
        selection_changed()

        planned, completed, topic_totals = summarize(sessions)
        percent = completed / GOAL_MINUTES
        totals.set(f"{len(visible)} of {len(sessions)} shown  ·  "
                   f"{planned} min planned  ·  "
                   f"{completed}/{GOAL_MINUTES} min completed ({percent:.0%})")
        progress.configure(value=min(completed, GOAL_MINUTES))
        topic_labels = [f"{topic}: {total} min" for topic, total in topic_totals]
        by_topic.set("  |  ".join(topic_labels))

    def add_session():
        try:
            session = make_session(title_input.get(), topic_input.get(),
                                   minutes_input.get())
        except ValueError as error:
            status.set(str(error))
            return
        sessions.append(session)
        title_input.set("")
        minutes_input.set("")
        search_input.set("")  # Show the new session even if a filter was active.
        refresh(len(sessions) - 1)
        status.set(f"Added {session[0]}.")
        title_entry.focus_set()

    def toggle_done():
        selected = tree.selection()
        if selected:
            index = int(selected[0])
            session = sessions[index]
            session[COMPLETED] = not session[COMPLETED]
            refresh(index)
            status.set(f"Updated {session[0]}.")

    def remove_session():
        selected = tree.selection()
        if selected:
            removed = sessions.pop(int(selected[0]))
            refresh()
            status.set(f"Removed {removed[0]}.")

    def selection_changed(event=None):
        selected = tree.selection()
        action_state = "normal" if selected else "disabled"
        toggle_button.configure(state=action_state)
        remove_button.configure(state=action_state)
        completed = bool(selected) and sessions[int(selected[0])][COMPLETED]
        toggle_button.configure(text="Mark planned" if completed else "Mark done")

    # bootstyle adds semantic button colours when ttkbootstrap is available.
    add_style = {"bootstyle": "primary"} if themed else {}
    done_style = {"bootstyle": "success"} if themed else {}
    remove_style = {"bootstyle": "danger"} if themed else {}
    widgets.Button(form, text="Add session", command=add_session,
                   **add_style).grid(sticky="ew")
    actions = widgets.Frame(plan)
    actions.grid(row=2, column=0, columnspan=4, sticky="w")
    toggle_button = widgets.Button(actions, command=toggle_done, **done_style)
    toggle_button.pack(side="left", padx=(0, 6))
    remove_button = widgets.Button(actions, text="Remove selected",
                                   command=remove_session, **remove_style)
    remove_button.pack(side="left")

    attach_tooltips(root, [
        (minutes_entry, f"Type a whole number from 1 to {MAX_MINUTES}, "
                        "or use the arrows to adjust it."),
        (search_entry, "Search session titles and topics. Clear the box to "
                       "show every session."),
        (sort_toggle, "Show the shortest sessions first. Turn this off to "
                      "return to the order you added them."),
        (toggle_button, "Select a row to mark it done. Choose Mark planned "
                        "to undo completion."),
        (remove_button, "Delete the selected session from the plan. "
                        "You can add it again if needed."),
        (progress, "Only time from completed sessions counts toward the "
                   f"{GOAL_MINUTES}-minute goal. Search does not change the total."),
    ])

    tree.bind("<<TreeviewSelect>>", selection_changed)
    search_input.trace_add("write", lambda *_: refresh())
    shortest_first.trace_add("write", lambda *_: refresh())
    for entry in (title_entry, minutes_entry):
        entry.bind("<Return>", lambda event: add_session())
    refresh()
    title_entry.focus_set()


def main():
    try:
        import ttkbootstrap as bootstrap
    except ModuleNotFoundError as error:
        if error.name != "ttkbootstrap":
            raise
        root = tk.Tk()
        build_planner(root)
    else:
        root = bootstrap.Window()
        build_planner(root, widgets=bootstrap)
    root.mainloop()


if __name__ == "__main__":
    main()

# DESK CHECK
# Add "Trace a loop" (Loops, 30 min) and "Validate a score" (Data and
# decisions, 15 min). The whole plan shows 45 minutes and 0 completed.
# Search for "score". Mark the only visible session done, then clear Search.
# The second session is Done and total progress reads 15/90 min (17%).
# Turn on Shortest first and remove the 15-minute row. The 30-minute session
# stays, and completed minutes return to 0. An invalid entry changes nothing.
#
# TRY IT: Predict the complete and filtered row lists before each click.
# DISCUSS: Why does sorting the index list let the data stay in entry order?
