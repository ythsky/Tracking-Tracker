"""
Top menu structure code
"""
import tkinter as tk
from tkinter import messagebox
from Core.add_item_sql import clear_all_items
from Core.list_generate import generate_from_sql
from Core.port_in_out import export_db, import_db


def create_menu(app):
    """
    Pure UI menu bar:
    - File: New Window / Exit
    - Help: About
    (All database-related functions have been removed originally)
    """

    menubar = tk.Menu(app.root)
    app.root.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)


    def new_window():
        messagebox.showinfo(
            "Info",
            "Food tracking system integrated with SQL.\n"
            "The program automatically saves content.\n"
            "Closing the window will NOT clear the content."
        )

    file_menu.add_command(label="Instruction", command=new_window)
    file_menu.add_command(label="Test", command=lambda: generate_from_sql())
    file_menu.add_command(label="Clear", command=lambda: clear_all_items())
    file_menu.add_command(label="Export Database", command=lambda: export_db(app))
    file_menu.add_command(label="Import Database", command=lambda: import_db(app))

    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=app.root.quit)


    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Info", menu=help_menu)


    def about():
        messagebox.showinfo(
            "About",
            "Food tracking system integrated with SQL\n"
            "Uses a database to store item data after creation and placement.\n"
            "Version V3.5 (I experienced two structure collapses — this is the third major rebuild, fifth conceptual result.)"
        )

    help_menu.add_command(label="About", command=about)