import tkinter as tk
from views.card_widget import CardWidget


class BoardView(tk.Frame):
    """Renders the full grid of CardWidgets. Inherits from tk.Frame.

    Calls card.get_display() on every card without checking the card's type —
    this is where Polymorphism is exercised at runtime."""

    def __init__(self, parent, board, on_card_click, **kwargs):
        super().__init__(parent, bg="#16213e", **kwargs)
        self._board = board
        self._on_card_click = on_card_click
        self._widgets = {}
        self._build()

    def _build(self):
        for widget in self.winfo_children():
            widget.destroy()
        self._widgets = {}
        for r in range(self._board.rows):
            for c in range(self._board.cols):
                card = self._board.get_card(r, c)
                cw = CardWidget(self, r, c, card, self._on_card_click)
                cw.grid(row=r, column=c, padx=4, pady=4)
                self._widgets[(r, c)] = cw

    def refresh(self):
        """Redraw all card widgets to reflect current model state."""
        for cw in self._widgets.values():
            cw.update_display()

    def rebuild(self, board):
        """Replace the board model and recreate all widgets (Play Again)."""
        self._board = board
        self._build()
