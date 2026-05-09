import tkinter as tk


class CardWidget(tk.Frame):
    """A single card button. Inherits from tk.Frame (library Inheritance).
    Visual state reflects the card model state."""

    HIDDEN_BG = "#4a90d9"
    REVEALED_BG = "#f0e68c"
    MATCHED_BG = "#90ee90"
    MATCHED_FG = "#2d5a2d"

    def __init__(self, parent, row, col, card, on_click, **kwargs):
        super().__init__(parent, bg="#16213e", **kwargs)
        self._row = row
        self._col = col
        self._card = card
        self._on_click = on_click

        self._btn = tk.Button(
            self,
            text="",
            width=6,
            height=3,
            font=("Arial", 14, "bold"),
            relief="raised",
            bd=2,
            command=self._clicked,
        )
        self._btn.pack(padx=2, pady=2)
        self.update_display()

    def _clicked(self):
        if not self._card.is_face_up and not self._card.is_matched:
            self._on_click(self._row, self._col)

    def update_display(self):
        """Refresh button appearance to match the card's current state."""
        if self._card.is_matched:
            self._btn.config(
                text=self._card.get_display(),
                bg=self.MATCHED_BG,
                fg=self.MATCHED_FG,
                state="disabled",
                disabledforeground=self.MATCHED_FG,
            )
        elif self._card.is_face_up:
            self._btn.config(
                text=self._card.get_display(),
                bg=self.REVEALED_BG,
                fg="#333333",
                state="normal",
            )
        else:
            self._btn.config(
                text="",
                bg=self.HIDDEN_BG,
                fg="#ffffff",
                state="normal",
            )
