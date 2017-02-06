import window as w
import functions as f
import tkinter as tk

f.import_crops(f.data)

def add_checkbox(Frame, row, label, gained_gold, long_gold=None):
    """ Given a seed and it's associated gold income, adds a checkbox to
    Frame (middle_frame). """
    if (long_gold != None):
        right_label = "{:5.2f} ({:6.2f})".format(gained_gold, long_gold)

    else:
        right_label = "{:6.2f}".format(gained_gold)

    num_letters = 35 - len(label) - len(right_label)
    label += " " * num_letters + right_label
 
    checkbox = tk.Checkbutton(Frame, text=label, bg='WHITE')
    checkbox.grid(row=row, sticky=tk.W)

def update_seeds():
    """ Called when the Update Seeds button is pressed. Takes the inputs given
    in the fields above the button (budget, season, date, max # seeds) and then
    fills the below frame with possible seeds and their associated gold income.
    """

    # Update status bar to reflect calculations are being made.
    w.status.config(text = "Calculating...")

    # Destroy existing choices.
    for checkbox in w.middle_frame.winfo_children():
        checkbox.destroy()

    # Get the crops that can be purchased based on input.
    paths = f.get_net_income(
        w.season_dropdown.get().lower(),
        int(w.date_entry.get()), 
        int(w.budget_entry.get()),
        int(w.num_seeds_entry.get()),
        f.data)

    # Check if crop net gold incomes were successfully retrieved.
    if paths == None:
        return

    # Add a new checkbox for each crop.
    row = 1
    for path in paths:
        add_checkbox(w.middle_frame, row, *path)
        row += 1

    # Update the status bar to reflect that calculations are finished.
    w.status.config(text = "Seeds updated! (Idle)")

# Associate a function with the Update Seeds button.
w.update_seeds_button.config(command = update_seeds)

# Open GUI and program.
w.root.geometry('250x500')
w.root.mainloop()