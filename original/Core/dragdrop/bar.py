"""
Timeline logic code
"""
import tkinter as tk
from tkinter import Menu
from Core.add_item_sql import update_item_bar_name


class TimelineBar:
    """
    Timeline bar (nameable, deletable, placeable for balls)
    - Left spawn area fixed at 200px
    - timeline width = canvasWidth - 400px
    - Color gradient: Green (>30) → Yellow (7~30) → Red (<7)
    - Ball horizontal position based on remaining days
    """

    LEFT_MARGIN = 200
    RIGHT_MARGIN = 200
    HEIGHT = 70

    def __init__(self, canvas, manager, y, bar_name):
        self.canvas = canvas
        self.manager = manager
        self.y = y
        self.bar_name = bar_name

        self.balls = []

        self.rect_ids = []
        self.text_ids = []

        self._draw()

        # Right-click menu
        self.menu = Menu(self.canvas, tearoff=0)
        self.menu.add_command(label="Delete This Bar", command=self._delete_self)

        # Bind right-click
        for rid in self.rect_ids:
            self.canvas.tag_bind(rid, "<Button-3>", self._show_menu)
        for tid in self.text_ids:
            self.canvas.tag_bind(tid, "<Button-3>", self._show_menu)


    def _draw(self):
        """
        Draw timeline
        """
        # Clear old graphics
        for r in self.rect_ids:
            self.canvas.delete(r)
        for t in self.text_ids:
            self.canvas.delete(t)
        self.rect_ids.clear()
        self.text_ids.clear()

        # Get width
        width = int(self.canvas.winfo_width())
        if width < 500:
            width = 800

        timeline_left = self.LEFT_MARGIN
        timeline_right = width - self.RIGHT_MARGIN
        timeline_width = timeline_right - timeline_left

        # Background bar (light gray)
        bar_bg = self.canvas.create_rectangle(
            timeline_left, self.y,
            timeline_right, self.y + self.HEIGHT,
            fill="#eeeeee", outline="#aaaaaa"
        )
        self.rect_ids.append(bar_bg)

        # Gradient (50 segments)
        segment_count = 50
        segment_width = timeline_width / segment_count

        start_color = (76, 175, 80)  # Green (#4caf50)
        mid_color = (255, 235, 59)  # Yellow (#ffeb3b)
        end_color = (244, 67, 54)  # Red (#f44336)

        def lerp(a, b, t):
            return a + (b - a) * t

        def blend(c1, c2, t):
            """
            Build single segment color
            """
            return (
                int(lerp(c1[0], c2[0], t)),
                int(lerp(c1[1], c2[1], t)),
                int(lerp(c1[2], c2[2], t))
            )

        for i in range(segment_count):
            t = i / (segment_count - 1)

            # Left half: Green to Yellow
            if t < 0.5:
                local_t = t / 0.5
                r, g, b = blend(start_color, mid_color, local_t)
            # Right half: Yellow to Red
            else:
                local_t = (t - 0.5) / 0.5
                r, g, b = blend(mid_color, end_color, local_t)

            color_hex = f"#{r:02x}{g:02x}{b:02x}"

            x1 = timeline_left + i * segment_width
            x2 = x1 + segment_width

            rect = self.canvas.create_rectangle(
                x1, self.y + 25,
                x2, self.y + 45,
                fill=color_hex, outline=""
            )
            self.rect_ids.append(rect)

        # Timeline name
        title = self.canvas.create_text(
            timeline_left,
            self.y + 12,
            text=self.bar_name,
            font=("Arial", 12, "bold"),
            anchor="w"
        )
        self.text_ids.append(title)

        # Ticks
        tick_values = ["50+", "30", "7", "0"]  # Left to right
        tick_positions = [
            0.05,        # 50 days
            20 / 50,     # 30 days
            43 / 50,     # 7 days
            0.98         # 0 days
        ]

        for value, pos in zip(tick_values, tick_positions):
            x = timeline_left + pos * timeline_width
            tick = self.canvas.create_text(
                x, self.y + 55,
                text=f"{value} days",
                font=("Arial", 9),
                anchor="center"
            )
            self.text_ids.append(tick)

        # Rebind right-click
        for rid in self.rect_ids:
            self.canvas.tag_bind(rid, "<Button-3>", self._show_menu)
        for tid in self.text_ids:
            self.canvas.tag_bind(tid, "<Button-3>", self._show_menu)

        # Reposition balls
        for b in self.balls:
            self._reposition_ball(b)


    def _compute_ball_x(self, remaining_days):
        """
        Map ball to timeline X coordinate
        """
        width = int(self.canvas.winfo_width())
        timeline_left = self.LEFT_MARGIN
        timeline_right = width - self.RIGHT_MARGIN
        timeline_width = timeline_right - timeline_left

        # Clamp
        days = max(0, min(remaining_days, 40))

        ratio = 1 - days / 40
        x = timeline_left + ratio * timeline_width
        return x


    def _reposition_ball(self, ball):
        """
        Position ball on timeline
        """
        x = self._compute_ball_x(ball.remaining_days)
        baseline_y = self.y + 35

        # Stacking detection
        same_x_count = 0
        for b in self.balls:
            if b is ball:
                continue
            bx, by = b._center()

            if abs(bx - x) < 5:
                same_x_count += 1

        y = baseline_y - same_x_count * 5

        ball.set_position(x, y)


    def snap_ball(self, ball):
        """
        Snap ball to this timeline.
        Handles:
        - Removing from left items
        - Removing from old timeline
        - Setting current_bar
        - Adding to this timeline
        - Repositioning ball based on remaining days
        """

        if ball in self.manager.items:
            self.manager.items.remove(ball)

        if ball.current_bar and ball.current_bar != self:
            ball.current_bar.remove_ball(ball)

        if ball not in self.balls:
            self.balls.append(ball)

        ball.current_bar = self
        update_item_bar_name(ball.name, self.bar_name)

        self._reposition_ball(ball)


    def _show_menu(self, event):
        """
        Show menu
        """
        self.menu.tk_popup(event.x_root, event.y_root)

    def _delete_self(self):
        """
        Delete timeline
        """
        for b in self.balls:
            b.current_bar = None
            update_item_bar_name(b.name, None)
            self.manager.return_ball_to_left(b)
        self.balls.clear()

        self.manager._delete_bar(self)

    def delete_graphics(self):
        """
        Delete timeline graphics
        """
        for rid in self.rect_ids:
            self.canvas.delete(rid)
        for tid in self.text_ids:
            self.canvas.delete(tid)

    def remove_ball(self, ball):
        """
        Remove ball from this timeline.
        Used when timeline is deleted / ball returns left / ball goes to trash.
        """
        if ball in self.balls:
            self.balls.remove(ball)
        ball.current_bar = None


    def redraw(self):
        """
        Redraw timeline
        """
        self._draw()
