import tkinter as tk
from views.menu_view import MenuView
from controllers.game_controller import GameController
from models.game_state import HighScoreTracker


class App:
    def __init__(self, root):
        self._root = root
        root.title("Memory Game")
        root.resizable(False, False)
        root.configure(bg="#1a1a2e")

        self._tracker = HighScoreTracker()
        self._container = tk.Frame(root, bg="#1a1a2e")
        self._container.pack()

        self._controller = GameController(
            root, self._container, self._show_menu, self._tracker
        )
        self._show_menu()

    def _show_menu(self):
        for w in self._container.winfo_children():
            w.destroy()
        MenuView(self._container, on_start=self._start_game).pack()

    def _start_game(self, mode, card_count, theme, name1, name2):
        for w in self._container.winfo_children():
            w.destroy()
        frame = self._controller.start(mode, card_count, theme, name1, name2)
        frame.pack()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
