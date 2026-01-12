"""
Connect to lower_module to create new items
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date


def custom_input_dialog(parent):
    """
    Create custom input dialog for entering item name and expiration date.

    This dialog contains:
    - Item name input field
    - Expiration date selection (year/month/day dropdowns)
    - Automatic date validation and day updates
    - Input auto-jump feature

    Args:
        parent: Parent window, usually the main window or the window calling this dialog

    Returns:
        tuple: If the user confirms input, return (item_name, expired_date)
               item_name (str): Name of the item
               expired_date (datetime.date): Expiration date
               If the user cancels or closes the dialog, return None

    Features:
        - Year field defaults to current year
        - Month dropdown contains 01-12
        - Day dropdown updates dynamically based on selected year & month
        - After entering the year, focus jumps to month
        - After selecting the month, focus jumps to day
    """
    dialog = tk.Toplevel(parent)
    dialog.title("Add Item")
    dialog.geometry("360x260")
    dialog.grab_set()

    today = date.today()
    current_year = today.year

    # Name
    ttk.Label(dialog, text="Item Name:").pack(pady=(10, 3))
    name_var = tk.StringVar()
    ttk.Entry(dialog, textvariable=name_var, width=30).pack()

    # Date section
    ttk.Label(dialog, text="Expiration Date:").pack(pady=(10, 3))

    date_frame = ttk.Frame(dialog)
    date_frame.pack(pady=5)

    # Year input
    ttk.Label(date_frame, text="Year").grid(row=0, column=0, padx=3)
    year_var = tk.StringVar(value=str(current_year))
    year_entry = ttk.Entry(date_frame, textvariable=year_var, width=6)
    year_entry.grid(row=1, column=0, padx=3)

    # Month
    ttk.Label(date_frame, text="Month").grid(row=0, column=1, padx=3)
    month_var = tk.StringVar()
    month_combo = ttk.Combobox(date_frame, textvariable=month_var, width=4, state="readonly")
    month_combo["values"] = [f"{i:02d}" for i in range(1, 13)]
    month_combo.grid(row=1, column=1, padx=3)

    # Day
    ttk.Label(date_frame, text="Day").grid(row=0, column=2, padx=3)
    day_var = tk.StringVar()
    day_combo = ttk.Combobox(date_frame, textvariable=day_var, width=4, state="readonly")
    day_combo.grid(row=1, column=2, padx=3)


    def update_days(*args):
        """
        Update the day dropdown based on selected year and month.

        This function dynamically calculates the number of days in the chosen
        month and updates the dropdown values. February is handled specially
        for leap years.

        Args:
            *args: Standard tkinter trace callback params (unused)

        Features:
            - Automatically calculates correct number of days per month
              (including leap year handling)
            - Leap year rule: divisible by 4 but not by 100, or divisible by 400
            - Corrects selected day if it exceeds the new month's valid range
            - Month groups:
                * 31 days: 1,3,5,7,8,10,12
                * 30 days: 4,6,9,11
                * 28/29 days: February (depending on leap year)

        Logic:
            1. Retrieve selected year/month
            2. Validate input
            3. Determine correct number of days
            4. Handle February leap years
            5. Update dropdown options
            6. Fix selected day if out of range

        Note:
            This function is auto-triggered via trace when year/month changes.
        """
        try:
            y = int(year_var.get())
            m = int(month_var.get())
        except:
            return

        # Determine days
        if m in [1, 3, 5, 7, 8, 10, 12]:
            days = 31
        elif m in [4, 6, 9, 11]:
            days = 30
        elif m == 2:
            # Leap year
            if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0):
                days = 29
            else:
                days = 28
        else:
            return

        day_combo["values"] = [f"{i:02d}" for i in range(1, days + 1)]

        # Auto-correct if selected day exceeds max
        if day_var.get():
            try:
                if int(day_var.get()) > days:
                    day_var.set(f"{days:02d}")
            except:
                pass

    # Refresh days when year or month changes
    year_var.trace_add("write", update_days)
    month_var.trace_add("write", update_days)

    # Initial day list
    update_days()


    def on_year_input(event):
        """Auto-jump to month field after entering 4 digits of year"""
        text = year_var.get()
        if len(text) == 4:
            month_combo.focus_set()

    year_entry.bind("<KeyRelease>", on_year_input)

    def on_month_selected(event):
        """Auto-jump to day selection after choosing month"""
        day_combo.focus_set()

    month_combo.bind("<<ComboboxSelected>>", on_month_selected)

    result = {"value": None}


    def on_confirm():
        """
        Internal validation of user input.

        This function reads the name and date (year/month/day) fields
        and performs the following validations:

        1. Item name must not be empty.
        2. Year/month/day fields must be filled.
        3. Year/month/day must be numeric.
        4. Date must be a real valid calendar date.
        5. Expiration date must not be earlier than today.

        If all validations pass:
            - Format the date as YYYY-MM-DD
            - Store (name, formatted_date) into result["value"]
            - Close the dialog

        If any validation fails:
            - Show a warning/error dialog
            - Do not close the dialog
        """
        name = name_var.get().strip()
        y = year_var.get().strip()
        m = month_var.get().strip()
        d = day_var.get().strip()

        # Name check
        if not name:
            messagebox.showwarning("Error", "Item name cannot be empty")
            return

        # Date completeness check
        if not (y and m and d):
            messagebox.showwarning("Error", "Please complete the date (year/month/day)")
            return

        # Convert to integers
        try:
            y, m, d = int(y), int(m), int(d)
        except:
            messagebox.showerror("Error", "Date must be numeric")
            return

        # Validate actual date
        try:
            chosen = date(y, m, d)
        except:
            messagebox.showerror("Error", "Invalid date, please check")
            return

        # Must not choose a date earlier than today
        if chosen < today:
            messagebox.showerror("Error", "Expiration date cannot be earlier than today")
            return

        day_str = f"{y:04d}-{m:02d}-{d:02d}"
        result["value"] = (name, day_str)
        dialog.destroy()

    ttk.Button(dialog, text="Confirm", command=on_confirm).pack(pady=10)
    ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack()

    dialog.wait_window()
    return result["value"]
