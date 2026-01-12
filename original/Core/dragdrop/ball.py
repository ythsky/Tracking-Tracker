"""
Core code for generating items
"""
import tkinter as tk
from datetime import datetime, date
from Core.dragdrop.tooltip import Tooltip
from Core.add_item_sql import insert_products
from .trash_bin import TrashBin


class DraggableBall:
    """
    Timeline system Ball:
    - name (item name)
    - expired_day (expiration date)
    - remaining_days (used for timeline mapping)
    - Ball color is fixed: blue, does not change based on days
    """

    RADIUS = 18
    COLOR = "#2196f3"   # Fixed blue

    def __init__(self, canvas, manager, name, expired_day, initial_x=100, initial_y=100):
        self.canvas = canvas
        self.manager = manager

        self.name = name
        self.expired_day = expired_day
        self.remaining_days = self._compute_remaining_days()

        # Belonging timeline
        self.current_bar = None

        # Graphic IDs
        self.ball_id = None
        self.text_id = None

        self.create_graphics(initial_x, initial_y)

        # Drag events
        self.canvas.tag_bind(self.ball_id, "<ButtonPress-1>", self._on_press)
        self.canvas.tag_bind(self.ball_id, "<B1-Motion>", self._on_drag)
        self.canvas.tag_bind(self.ball_id, "<ButtonRelease-1>", self._on_release)

        self.canvas.tag_bind(self.text_id, "<ButtonPress-1>", self._on_press)
        self.canvas.tag_bind(self.text_id, "<B1-Motion>", self._on_drag)
        self.canvas.tag_bind(self.text_id, "<ButtonRelease-1>", self._on_release)

        # Tooltip on hover
        self.canvas.tag_bind(self.ball_id, "<Enter>", self._on_hover)
        self.canvas.tag_bind(self.ball_id, "<Leave>", self._on_leave)

        self.canvas.tag_bind(self.text_id, "<Enter>", self._on_hover)
        self.canvas.tag_bind(self.text_id, "<Leave>", self._on_leave)


    def _compute_remaining_days(self):
        """
        Compute remaining days
        :return: days
        """
        try:
            d = datetime.strptime(self.expired_day, "%Y-%m-%d").date()
            return (d - date.today()).days
        except:
            return 30


    def create_graphics(self, x, y):
        """
        Generate item graphics
        :param x: x position
        :param y: y position
        :return: None
        """
        # Tooltip text
        self.tooltip = Tooltip(
            self.canvas.winfo_toplevel(),
            self._tooltip_text()
        )

        r = self.RADIUS

        self.ball_id = self.canvas.create_oval(
            x - r, y - r, x + r, y + r,
            fill=self.COLOR, outline="black", width=2
        )

        self.text_id = self.canvas.create_text(
            x, y,
            text=self.name,
            font=("Arial", 10, "bold")
        )

        self.canvas.tag_raise(self.ball_id)
        self.canvas.tag_raise(self.text_id)


    def _on_press(self, event):
        """
        Drag logic (press)
        """
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def _on_drag(self, event):
        """
        Drag logic (move)
        """
        self.canvas.tag_raise(self.ball_id)
        self.canvas.tag_raise(self.text_id)

        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y

        self.canvas.move(self.ball_id, dx, dy)
        self.canvas.move(self.text_id, dx, dy)

        self.drag_start_x = event.x
        self.drag_start_y = event.y


    def _on_release(self, event):
        """
        Release item logic
        """

        # Try snapping to timeline
        if self.manager.try_snap_to_bar(self):
            return

        # Try snapping to trash
        if self.manager.try_snap_to_trash(self):
            return

        # If both fail, return to left side
        self.manager.return_ball_to_left(self)


    def set_position(self, x, y):
        """
        Set item position
        """
        r = self.RADIUS
        self.canvas.coords(self.ball_id, x - r, y - r, x + r, y + r)
        self.canvas.coords(self.text_id, x, y)

        # Ensure ball stays above after timeline redraw
        self.canvas.tag_raise(self.ball_id)
        self.canvas.tag_raise(self.text_id)

    def _center(self):
        """
        Get item center coordinates
        """
        x1, y1, x2, y2 = self.canvas.coords(self.ball_id)
        return (x1 + x2) / 2, (y1 + y2) / 2

    def delete_graphics(self):
        """
        Delete item graphical elements
        """
        if self.ball_id:
            self.canvas.delete(self.ball_id)
        if self.text_id:
            self.canvas.delete(self.text_id)

    def rebuild_graphics(self):
        """
        Restore from trash
        """
        self.remaining_days = self._compute_remaining_days()

        # Create new graphics
        self.create_graphics(80, 80)

        # Rebind events
        for id in (self.ball_id, self.text_id):
            self.canvas.tag_bind(id, "<ButtonPress-1>", self._on_press)
            self.canvas.tag_bind(id, "<B1-Motion>", self._on_drag)
            self.canvas.tag_bind(id, "<ButtonRelease-1>", self._on_release)
            self.canvas.tag_bind(id, "<Enter>", self._on_hover)
            self.canvas.tag_bind(id, "<Leave>", self._on_leave)

    def _tooltip_text(self):
        """
        Tooltip content
        """
        return (
            f"Name: {self.name}\n"
            f"Expiration Date: {self.expired_day}\n"
            f"Remaining Days: {self.remaining_days} days"
        )

    """Checking trash logic, abandoned"""
    def _on_hover(self, event):
        bx, by = self._center()
        r = self.RADIUS

        # Convert canvas coordinate to absolute screen coordinate
        screen_x = self.canvas.winfo_rootx() + bx + r + 4
        screen_y = self.canvas.winfo_rooty() + by + r + 4

        self.tooltip.show(screen_x, screen_y)

    def _on_leave(self, event):
        self.tooltip.hide()
