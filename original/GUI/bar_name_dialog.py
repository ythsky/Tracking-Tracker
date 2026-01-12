"""
Create Timeline
"""
import tkinter as tk
from tkinter import ttk, messagebox


def bar_name_dialog(parent):
    """
    Popup input dialog, return bar_name
    """
    dialog = tk.Toplevel(parent)
    dialog.title("Add New Bar")
    dialog.geometry("260x130")
    dialog.grab_set()

    ttk.Label(dialog, text="Please enter category name:").pack(pady=10)

    name_var = tk.StringVar()
    entry = ttk.Entry(dialog, textvariable=name_var, width=20)
    entry.pack()
    entry.focus()

    result = {"value": None}

    def confirm():
        """
        Check if user entered content
        """
        name = name_var.get().strip()
        if not name:
            messagebox.showwarning("Error", "Name cannot be empty")
            return
        result["value"] = name
        dialog.destroy()

    ttk.Button(dialog, text="Confirm", command=confirm).pack(pady=8)
    ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack()

    dialog.wait_window()
    return result["value"]