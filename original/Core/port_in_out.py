"""
SQL export/import system
"""
import os
import shutil
from tkinter import filedialog, messagebox
from Core.add_item_sql import _db_path

def export_db(app):
    """Export database (Utils/test.db)"""
    export_path = filedialog.asksaveasfilename(
        title="Export Database",
        defaultextension=".db",
        filetypes=[("SQLite DB File", "*.db")]
    )
    if not export_path:
        return

    try:
        shutil.copyfile(_db_path(), export_path)
        messagebox.showinfo("Success", f"Database exported to:\n{export_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Export failed:\n{e}")


def import_db(app):
    """
    Import database and refresh UI
    """
    import_path = filedialog.askopenfilename(
        title="Select Database File",
        filetypes=[("SQLite DB File", "*.db")]
    )
    if not import_path:
        return

    confirm = messagebox.askyesno(
        "Confirm Import",
        "Importing will overwrite the current database. Continue?"
    )
    if not confirm:
        return

    try:
        shutil.copyfile(import_path, _db_path())
        messagebox.showinfo("Success", "Database imported successfully! Please restart the program to see data.")

        # Refresh UI automatically
        app.lower_model.update_sql_stats()
        app.lower_model.update_trash_preview()

    except Exception as e:
        messagebox.showerror("Error", f"Import failed:\n{e}")