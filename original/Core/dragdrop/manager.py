"""
Extremely important
Code linking display structure and functionality
Do not modify
"""
import tkinter as tk
from .ball import DraggableBall
from .bar import TimelineBar
from .trash_bin import TrashBin
from Core.list_generate import generate_from_sql
from Core.add_item_sql import update_item_bar_name

class DragDropManager:
    """
    Core manager for Timeline multi-axis system:
    - Create/delete timelines
    - Handle ball drag, snapping, return to left
    - Automatically compute ball X coordinate based on remaining days
    - Auto-shift timeline positions upward after deletion
    """

    LEFT_AREA_WIDTH = 200
    TIMELINE_GAP = 120   # Vertical gap between timelines

    def __init__(self, main_window, canvas):
        self.main_window = main_window  # ⭐ Save MainWindow
        self.canvas = canvas

        self.items = []
        self.bars = []

        # Correctly create trash bin
        self.trash_bin = TrashBin(self.main_window, self)


    def create_ball(self, name, expired_day):
        """Create a new food ball (spawn in left area)"""
        ball = DraggableBall(self.canvas, self, name, expired_day, 0, 0)
        self.items.append(ball)
        self.rebuild_left_area()
        return ball

    def _on_release(self, event):
        """Snapping logic"""
        # Try snapping to timeline
        if self.manager.try_snap_to_bar(self):
            return

        # Try snapping to trash bin
        if self.manager.try_snap_to_trash(self):
            return

        # Otherwise return to left
        self.manager.return_ball_to_left(self)

    def return_ball_to_left(self, ball):
        """
        Put ball back into the left spawn area.
        Responsible for:
        - Removing from timeline if present
        - Ensuring it is in items list
        - Rebuilding left area layout
        """

        # Remove from timeline if needed
        if ball.current_bar:
            ball.current_bar.remove_ball(ball)
            ball.current_bar = None

        # Add back to items list
        if ball not in self.items:
            update_item_bar_name(ball.name, None)
            self.items.append(ball)

        self.rebuild_left_area()

    def rebuild_left_area(self):
        """Rebuild left spawn list"""
        left_balls = [b for b in self.items if b.current_bar is None]

        base_x = self.LEFT_AREA_WIDTH // 2
        base_y = 60
        gap = 60

        for i, ball in enumerate(left_balls):
            ball.set_position(base_x, base_y + i * gap)


    def add_bar(self, bar_name):
        """Add a new timeline"""
        y = 50 + len(self.bars) * self.TIMELINE_GAP
        bar = TimelineBar(canvas=self.canvas, manager=self, y=y, bar_name=bar_name)
        self.bars.append(bar)

    def _delete_bar(self, bar):
        """
        Logic for deleting a timeline
        """
        if bar not in self.bars:
            return

        bar.delete_graphics()

        self.bars.remove(bar)

        # Reposition remaining timelines
        for i, b in enumerate(self.bars):
            b.y = 50 + i * self.TIMELINE_GAP
            b.redraw()

        # Rebuild left area
        self.rebuild_left_area()


    def redraw_timelines(self):
        """Redraw all timelines when window size changes"""

        for bar in self.bars:
            bar.redraw()

        # After timeline redraw, reposition balls on them
        for ball in self.items:
            if ball.current_bar:
                ball.current_bar._reposition_ball(ball)

    def try_snap_to_bar(self, ball):
        """
        Try snapping ball onto a timeline
        """
        bx, by = ball._center()

        for bar in self.bars:
            if abs(by - bar.y) < 40:
                bar.snap_ball(ball)
                return True

        return False

    def try_snap_to_trash(self, ball):
        """
        Check whether ball enters trash bin hitbox
        """

        bx, by = ball._center()

        # Trash bin widget screen coordinates
        bin_widget = self.trash_bin.frame
        x1 = bin_widget.winfo_rootx()
        y1 = bin_widget.winfo_rooty()
        x2 = x1 + bin_widget.winfo_width()
        y2 = y1 + bin_widget.winfo_height()

        # Canvas → screen coordinate
        screen_x = self.canvas.winfo_rootx() + bx
        screen_y = self.canvas.winfo_rooty() + by

        # Check if ball is inside trash area
        if x1 <= screen_x <= x2 and y1 <= screen_y <= y2:
            self.trash_bin.put_ball_in_trash(ball)
            return True

        return False


    def load_from_sql_initial(self):
        """
        Initial loading on program start:
        - Do not clear UI (since no balls/timelines created yet)
        - Create timelines + balls directly from SQL data
        """

        items_list, bar_name_list = generate_from_sql()

        # Create timelines
        for bar_name in bar_name_list:
            self.add_bar(bar_name)

        # Create balls
        for item_name, expired_day, bar_name in items_list:
            ball = self.create_ball(item_name, expired_day)

            # If ball belongs to timeline, snap it
            for bar in self.bars:
                if bar.bar_name == bar_name:
                    bar.snap_ball(ball)
                    break

        # Rebuild left spawn area
        self.rebuild_left_area()
