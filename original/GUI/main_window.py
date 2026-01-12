"""
Main module design for display area, main frame uses Grid
"""
import tkinter as tk
from tkinter import ttk
from .menu import create_menu
from .upper_model import UpperModule
from .lower_module import LowerModule


class StorageTracker:
    """
    Main window (pure UI version)
    Does not load or save database.
    Closing the window clears all content.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Food Management System")
        # Force root not to expand due to internal widgets
        self.root.grid_propagate(False)

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        win_w = int(screen_w * 0.75)
        win_h = int(screen_h * 0.75)

        pos_x = (screen_w - win_w) // 2
        pos_y = (screen_h - win_h) // 2

        self.root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
        self.root.minsize(800, 600)

        self.root.grid_rowconfigure(0, weight=3, minsize=0)
        self.root.grid_rowconfigure(1, weight=2, minsize=0)
        self.root.grid_columnconfigure(0, weight=1)

        self.upper_model = UpperModule(self.root,)

        self.lower_model = LowerModule(self.root, self.upper_model.manager)

        self.lower_model.update_sql_stats()

        create_menu(self)


    def run(self):
        """
        Main loop runner
        """

        self.root.mainloop()