"""
Upper part canvas structure code
"""
import tkinter as tk
from tkinter import ttk
from Core.dragdrop.manager import DragDropManager
from Core.dragdrop.trash_bin import TrashBin
from .bar_name_dialog import bar_name_dialog


class UpperModule:
    """
    Upper GUI area of Timeline version.
    Contains:
    - Canvas (left birth area + right multiple timelines)
    - Add new bar button
    - Trash bin
    """


    def __init__(self, parent):
        self.parent = parent

        # Upper main frame
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Frame row/column config
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Top controls (add new bar button)
        self._create_top_controls()

        # Canvas area (drag + timeline)
        self._create_canvas_area()


    def _create_top_controls(self):
        """
        Add timeline settings
        """
        top_bar = ttk.Frame(self.frame)
        top_bar.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        add_btn = ttk.Button(top_bar, text="Add Bar", command=self._add_bar)
        add_btn.grid(row=0, column=0, padx=5)


    def _add_bar(self):
        """
        Popup input name → add a new bar
        """
        name = bar_name_dialog(self.frame)
        if not name:
            return
        self.manager.add_bar(name)
        self.manager.redraw_timelines()


    def _create_canvas_area(self):
        """
        Main creation logic of upper canvas area
        """
        # Container frame
        container = ttk.Frame(self.frame)
        container.grid(row=1, column=0, sticky="nsew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Canvas (main drawing area)
        self.canvas = tk.Canvas(container, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        scroll_y = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=scroll_y.set)

        # Correctly create Manager (must pass parent and canvas)
        from Core.dragdrop.manager import DragDropManager
        self.manager = DragDropManager(self.frame, self.canvas)

        # Create trash bin and attach to manager
        from Core.dragdrop.trash_bin import TrashBin
        self.trash_bin = TrashBin(self.frame, self.manager)
        self.manager.trash_bin = self.trash_bin

        # On program start, load timelines and balls from SQL (initial load version)
        try:
            self.manager.load_from_sql_initial()
        except Exception as e:
            print("Error occurred while loading from SQL:", e)

        # Dynamic redraw timeline
        self.canvas.bind("<Configure>", self._on_canvas_resize)


    def _on_canvas_resize(self, event):
        """
        When window resizes, timeline width needs update,
        and ball positions need to be remapped to timeline.
        """
        if hasattr(self, "manager"):
            self.manager.redraw_timelines()
