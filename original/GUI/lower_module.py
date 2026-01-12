"""
Main module design for lower area, main frame uses Grid
"""
import tkinter as tk
from tkinter import ttk
from GUI.add_item import custom_input_dialog
from Core.add_item_sql import insert_products

from PIL import Image, ImageTk
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_PATH_BAG = os.path.join(BASE_DIR, "Utils", "bag.png")  # Corresponding image path

bag_img = Image.open(IMG_PATH_BAG)
bag_img = bag_img.resize((150, 200))  # Adjust paper bag size

class LowerModule:
    """
    Lower section layout with three blocks (width: 20% / 40% / 40%)
    Must use grid layout only; pack is disabled to ensure horizontal arrangement.
    """

    def __init__(self, parent, manager):
        self.parent = parent
        self.manager = manager

        # Save original image for continuous resizing
        self.bag_img_original = bag_img
        self.bag_tk = ImageTk.PhotoImage(bag_img)

        # Bind window size change (adaptive resizing core)
        self.parent.bind("<Configure>", self._on_resize)

        # Entire lower frame
        self.frame = ttk.Frame(parent, relief="solid", borderwidth=1)
        self.frame.grid(row=1, column=0, sticky="nsew")
        self.frame.grid_propagate(False)

        # Configure three column proportions (1:2:2)
        self.frame.grid_columnconfigure(0, weight=1)   # 20%
        self.frame.grid_columnconfigure(1, weight=2)   # 40%
        self.frame.grid_columnconfigure(2, weight=2)   # 40%
        self.frame.grid_rowconfigure(0, weight=1)

        # Create the three blocks
        self._build_left_block()
        self._build_middle_block()
        self._build_right_block()


    def _build_left_block(self):
        """
        Main structure and internal logic of left block
        """
        left = ttk.Frame(self.frame, relief="solid", borderwidth=1)
        left.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        left.grid_rowconfigure(0, weight=1)
        left.grid_columnconfigure(0, weight=1)
        left.grid_columnconfigure(1, weight=1)

        # Save label (image)
        self.bag_label = tk.Label(left, image=self.bag_tk)
        self.bag_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        # Add button
        self.add_btn = ttk.Button(
            left,
            text="Add Item",
            command=self.add_item_via_dialog,
            width=40,
            padding=(0, 16)
        )
        self.add_btn.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    def _on_resize(self, event):
        """
        Automatically adjust button and image size on window resize
        """

        # Width of left region (1/3 of lower frame)
        left_width = self.frame.winfo_width() // 3

        if left_width <= 50:
            return  # Prevent errors if window is too small

        # Resize image
        # Target width is 25% of left_width
        img_width = max(40, int(left_width * 0.25))
        img_height = int(img_width * 1.33)  # Original ratio 150x200 → 1 : 1.33

        resized = self.bag_img_original.resize((img_width, img_height))
        self.bag_tk = ImageTk.PhotoImage(resized)
        self.bag_label.configure(image=self.bag_tk)

        # Adjust button width
        btn_width = max(10, int(left_width / 10))
        self.add_btn.configure(width=btn_width)

        # Adjust vertical padding
        pad_y = max(8, int(left_width / 40))
        self.add_btn.configure(padding=(0, pad_y))

    # Create ball
    def add_item_via_dialog(self):
        """
        Open input dialog, write into SQL, generate ball, refresh statistics
        """
        data = custom_input_dialog(self.frame)
        if not data:
            return  # User canceled

        name, expired_day = data

        # Write to database
        insert_products(name, expired_day)

        # Generate new ball
        self.manager.create_ball(name, expired_day)

        # Refresh stats
        self.update_sql_stats()


    def _build_middle_block(self):
        """
        Main structure and internal logic of middle block
        """
        middle = ttk.Frame(self.frame, relief="solid", borderwidth=1)
        middle.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        middle.grid_columnconfigure(0, weight=1)
        middle.grid_rowconfigure(1, weight=1)
        middle.grid_propagate(False)

        # Title
        title = ttk.Label(middle, text="Information Display", font=("Arial", 10, "bold"))
        title.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # Scrollbar
        scroll = ttk.Scrollbar(middle)
        scroll.grid(row=1, column=1, sticky="ns")

        # Text display (read-only)
        self.stats_text = tk.Text(
            middle,
            wrap="word",
            font=("Arial", 9),
            state="disabled"
        )
        self.stats_text.grid(row=1, column=0, sticky="nsew", padx=(5, 0), pady=5)

        scroll.config(command=self.stats_text.yview)
        self.stats_text.config(yscrollcommand=scroll.set)

    def update_sql_stats(self):
        """
        Read statistics from SQL and display them in scrollable text box
        """
        from Core.sql_stats import get_sql_stats
        stats = get_sql_stats()

        def lst_text(lst):
            """
            Display internal SQL variable statistics
            """
            if not lst:
                return "(none)"
            return "\n".join(f"- {item}" for item in lst)

        text = (
            f"Total: {sum(len(v) for v in stats.values())}\n\n"
            f"> 30 days ({len(stats['>30'])}):\n{lst_text(stats['>30'])}\n\n"
            f"7 ~ 30 days ({len(stats['7~30'])}):\n{lst_text(stats['7~30'])}\n\n"
            f"< 7 days ({len(stats['<7'])}):\n{lst_text(stats['<7'])}\n\n"
            f"Expired ({len(stats['expired'])}):\n{lst_text(stats['expired'])}"
        )

        self.stats_text.config(state="normal")
        self.stats_text.delete("1.0", "end")
        self.stats_text.insert("end", text)
        self.stats_text.config(state="disabled")


    def _build_right_block(self):
        """
        Main structure and internal logic of right block
        """
        right = ttk.Frame(self.frame, relief="solid", borderwidth=1)
        right.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1)
        right.grid_propagate(False)

        title = ttk.Label(right, text="Trash Preview", font=("Arial", 10, "bold"))
        title.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        refresh_btn = ttk.Button(right, text="Refresh", command=self.update_trash_preview)
        refresh_btn.grid(row=0, column=1, sticky="e", padx=5, pady=5)

        # Trash preview Text + Scrollbar
        scroll = ttk.Scrollbar(right)
        scroll.grid(row=1, column=1, sticky="ns")

        self.trash_preview = tk.Text(
            right,
            wrap="word",
            font=("Arial", 9),
            state="disabled"
        )
        self.trash_preview.grid(row=1, column=0, sticky="nsew", padx=(5, 0), pady=5)

        scroll.config(command=self.trash_preview.yview)
        self.trash_preview.config(yscrollcommand=scroll.set)

    def update_trash_preview(self):
        """
        Trash display function; if trash bin is empty show (none),
        refresh content through refresh button
        """
        self.update_sql_stats()
        trash_list = self.manager.trash_bin.trash_list

        if not trash_list:
            text = "(no trash)"
        else:
            lines = []
            for b in trash_list:
                lines.append(f"- {b.name} ({b.expired_day})")
            text = "\n".join(lines)

        self.trash_preview.config(state="normal")
        self.trash_preview.delete("1.0", "end")
        self.trash_preview.insert("end", text)
        self.trash_preview.config(state="disabled")