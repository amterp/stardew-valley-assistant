# Author:           Alexander M. Terp
# Date created:     January, 2016
# Description:      Contains code responsible for the GUI for SVA.

from tkinter import *
from tkinter import ttk

def clear():
    """ Clears all the input fields, including drop downs and checkboxes. """
    season_dropdown.set("")

    entries = ["date", "budget", "num_seeds"]
    for entry in entries:
        eval(entry + "_entry.delete(0, END)")

root = Tk()
Grid.rowconfigure(root, 0, weight=0)
Grid.columnconfigure(root, 0, weight=1)

"""
Define top frame. Will contain:
    - Season input segment.
    - Date input segment.
    - Budget input segment.
    - Number of seeds input segment.
    - Instructions for next frame (picking crops). """
top_frame = Frame(root)

# Define cascading menu bar.
menu_bar = Menu(top_frame)
root.config(menu=menu_bar)
edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Clear", command=clear)

# Define season segment.
season_label = Label(top_frame, text='Season:')
season_dropdown = ttk.Combobox(top_frame)
season_dropdown['values'] = ("Spring", "Summer", "Fall")
season_dropdown.config(width=15)

# Place season segment.
season_label.grid(row=0, pady=3, padx=3, sticky=W+N)
season_dropdown.grid(row=0, column=1, pady=3, padx=3, sticky=E+N)


# Define date segment.
date_label = Label(top_frame, text='Date:')
date_entry = Entry(top_frame, justify=CENTER)
date_entry.config(width=18)

# Place date segment.
date_label.grid(row=1, pady=3, padx=3, sticky=W+N)
date_entry.grid(row=1, column=1, pady=3, padx=3, sticky=E+N)


# Define budget segment.
budget_label = Label(top_frame, text='Budget:')
budget_entry = Entry(top_frame, justify=CENTER)
budget_entry.config(width=18)

# Place budget segment.
budget_label.grid(row=2, pady=3, padx=3, sticky=W+N)
budget_entry.grid(row=2, column=1, pady=3, padx=3, sticky=E+N)


# Define num seeds segment.
num_seeds_label = Label(top_frame, text='Max # seeds:')
num_seeds_entry = Entry(top_frame, justify=CENTER)
num_seeds_entry.config(width=18)

# Place num seeds segment.
num_seeds_label.grid(row=3, pady=3, padx=3, sticky=W+N)
num_seeds_entry.grid(row=3, column=1, pady=3, padx=3, sticky=E+N)


# Define and place Update Seeds button.
update_seeds_button = Button(top_frame, text="Update seeds", command=clear, bd=4)
update_seeds_button.grid(row=4, columnspan=2, pady=2)

# Define crops to buy segment.
seeds_to_buy_label = Label(top_frame, text="Check the seeds you're willing and\nable to buy:")

# Place crops to buy segment.
seeds_to_buy_label.grid(row=5, pady=3, padx=3, columnspan=2)


# Pack top frame.
top_frame.pack()


"""
Define middle frame. Will contain:
    - A number of checkboxes for crops and their corresponding 
      net gold income per day to the right. """
middle_frame = Frame(root, relief=SUNKEN)
middle_frame.configure(bg="WHITE", bd=1)

# Pack middle frame.
middle_frame.pack(padx=20, fill=X)


# Define and place status bar.
status = Label(root, text='Idle', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)