"""
This is the full core code of the main trash bin functionality.
Please do not modify lightly.
"""
import os
import tkinter as tk
from tkinter import Menu
from Core.add_item_sql import delete_item

from Core.add_item_sql import update_item_bar_name

from PIL import Image, ImageTk

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMG_PATH = os.path.join(BASE_DIR, "Utils", "MGb360-Front-View.PNG")
IMG_PATH_2 = os.path.join(BASE_DIR, "Utils", "MGb360-Front-View2.PNG")

# Save original images (for real-time resizing)
img_original = Image.open(IMG_PATH)
img_hover_original = Image.open(IMG_PATH_2)

# Initial scaling
img = img_original.resize((306, 126))
img_2 = img_hover_original.resize((306, 126))


class TrashBin:
    """
    Pure UI Trash Bin
    - Drag into trash → soft delete (hide ball)
    - Right-click menu:
        1. Undo all trash
        2. Empty trash bin (permanently delete Ball objects)
    """

    def __init__(self, main_window, manager):
        self.main_window = main_window
        self.manager = manager
        self.img_original = img_original
        self.img_hover_original = img_hover_original

        # Initial images
        self.trash_img = ImageTk.PhotoImage(img)
        self.trash_img_2 = ImageTk.PhotoImage(img_2)

        # Trash bin UI
        self.frame = tk.Frame(main_window, bd=2)
        self.frame.place(relx=1.0, rely=1.0, anchor="se", relwidth=0.18, relheight=0.12)

        self.label = tk.Label(self.frame, image=self.trash_img)
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        # Store soft-deleted balls
        self.trash_list = []

        # Right-click menu
        self.menu = Menu(self.frame, tearoff=0)
        self.menu.add_command(label="Undo All Trash", command=self.undo)
        self.menu.add_command(label="Empty Trash Bin", command=self.clear_trash)

        self.frame.bind("<Button-3>", self._show_menu)
        self.label.bind("<Button-3>", self._show_menu)

        # Hover effects
        self.label.bind("<Enter>", self.on_hover)
        self.label.bind("<Leave>", self.on_leave)

        # Delay binding resize to avoid tiny startup size
        self.main_window.after(50, lambda: self.main_window.bind("<Configure>", self._on_resize))

        # Manual initial resize
        self.main_window.after(100, self._on_resize)

    def get_area(self):
        """
        Old test code, now deprecated
        """
        x = self.frame.winfo_rootx()
        y = self.frame.winfo_rooty()
        w = self.frame.winfo_width()
        h = self.frame.winfo_height()
        return x, y, w, h

    def on_hover(self, event):
        """
        Update trash bin image on hover
        """
        print("on")
        self.label.config(image=self.trash_img_2)

    def on_leave(self, event):
        """
        Restore trash bin image when leaving hover
        """
        print("out")
        self.label.config(image=self.trash_img)

    def _on_resize(self, event=None):
        """Automatically resize trash bin images on window resize"""

        frame_width = max(150, self.frame.winfo_width())
        frame_height = max(60, self.frame.winfo_height())

        # Resize proportionally
        new_w = int(frame_width)
        new_h = int(frame_height)

        # Prevent extreme scaling
        new_w = min(new_w, 600)
        new_h = min(new_h, 300)

        # Resize normal image
        resized_normal = self.img_original.resize((new_w, new_h))
        self.trash_img = ImageTk.PhotoImage(resized_normal)

        # Resize hover image
        resized_hover = self.img_hover_original.resize((new_w, new_h))
        self.trash_img_2 = ImageTk.PhotoImage(resized_hover)

        # Update UI
        if self.label == self.frame.focus_get():
            self.label.config(image=self.trash_img_2)
        else:
            self.label.config(image=self.trash_img)

        self.label.place(relx=0.5, rely=0.5, anchor="center")


    def _show_menu(self, event):
        """Right-click menu"""
        self.menu.tk_popup(event.x_root, event.y_root)


    def put_ball_in_trash(self, ball):
        """
        Called by DragDropManager:
        - Ball is hidden from canvas but object remains in memory
        """
        if ball.current_bar:
            ball.current_bar.remove_ball(ball)
        if ball in self.manager.items:
            self.manager.items.remove(ball)
        ball.delete_graphics()

        if ball not in self.trash_list:
            self.trash_list.append(ball)
        ball.tooltip.hide()

        print(len(self.trash_list))

        # Deprecated preview refresh
        # self.main_window.lower_module.update_trash_preview()


    def undo(self):
        """
        Undo: restore all deleted balls
        """
        if not self.trash_list:
            return

        for ball in list(self.trash_list):
            ball.rebuild_graphics()
            ball.current_bar = None

            self.trash_list.remove(ball)

            # Return to left area
            self.manager.items.append(ball)
            self.manager.rebuild_left_area()

        print(len(self.trash_list))

        # self.main_window.lower_module.update_trash_preview()


    def clear_trash(self):
        """
        Empty trash bin (permanently delete Ball objects)
        """
        for ball in self.trash_list:
            delete_item(ball.name)
            ball.delete_graphics()

        self.trash_list.clear()

        # Refresh SQL stats if desired
        # self.main_window.lower_module.update_trash_preview()
        # self.main_window.lower_module.update_sql_stats()


    def clear_visual_only(self):
        """
        Clear only visual remnants (for UI cleanup)
        """
        for ball in self.trash_list:
            ball.delete_graphics()
        self.trash_list.clear()
