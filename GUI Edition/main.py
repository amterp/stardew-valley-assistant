import window as w
import functions as f
import tkinter as tk

f.import_crops(f.data)

def add_checkbox(Frame, row, label, gained_gold, long_gold=None):
    if (long_gold != None):
        right_label = "{:5.2f} ({:6.2f})".format(gained_gold, long_gold)

    else:
        right_label = "{:6.2f}".format(gained_gold)

    num_letters = 35 - len(label) - len(right_label)
    label += " " * num_letters + right_label
 
    checkbox = tk.Checkbutton(Frame, text=label, bg='WHITE')
    checkbox.grid(row=row, sticky=tk.W)

def update_seeds():

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

    # Add a new checkbox for each crop.
    row = 1
    for path in paths:
        add_checkbox(w.middle_frame, row, *path)
        row += 1

w.update_seeds_button.config(command = update_seeds)

# Open GUI and program.
w.root.geometry('250x500')
w.root.mainloop()