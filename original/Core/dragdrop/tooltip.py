"""
This is the core code for the tooltip
"""
import tkinter as tk


class Tooltip:
    """
    Advanced Tooltip (bubble tooltip)
    - Beige background (#f5f5dc)
    - Black text
    - Rounded background
    - Instant show / instant hide
    - Fixed at bottom-right of the ball
    """

    BG_COLOR = "#f5f5dc"   # Beige
    FG_COLOR = "black"     # Text color
    FONT = ("Arial", 7)

    def __init__(self, parent, text):
        self.parent = parent        # Root window
        self.text = text
        self.tip = None

    def show(self, x, y):
        """
        Show logic
        """
        self.hide()

        self.tip = tk.Toplevel(self.parent)
        self.tip.withdraw()
        self.tip.overrideredirect(True)
        self.tip.attributes("-topmost", True)

        canvas = tk.Canvas(self.tip, bg=self.BG_COLOR,
                           highlightthickness=0, bd=0)
        canvas.pack(fill="both", expand=True)

        padding = 6
        text_id = canvas.create_text(
            padding + 4, padding + 4,
            text=self.text,
            fill=self.FG_COLOR,
            font=self.FONT,
            anchor="nw"
        )
        bbox = canvas.bbox(text_id)
        w = bbox[2] + padding * 2
        h = bbox[3] + padding * 2

        self.tip.geometry(f"{w}x{h}+{int(x)}+{int(y)}")

        r = 8
        canvas.create_round_rectangle(
            0, 0, w, h, r,
            fill=self.BG_COLOR,
            outline=self.BG_COLOR
        )
        canvas.tag_raise(text_id)

        # Critical line: show the window
        self.tip.deiconify()

    def hide(self):
        """Hide tooltip"""
        if self.tip:
            try:
                self.tip.destroy()
            except:
                pass
            self.tip = None


    # Add round-rectangle method to Canvas
    def _create_round_rect(self, x1, y1, x2, y2, r, **kwargs):
        """Add round_rectangle drawing ability to Canvas"""
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)


    # Bind the method to tk.Canvas
    tk.Canvas.create_round_rectangle = _create_round_rect
