class Card:
    """Base card class. Demonstrates Encapsulation (private state) and is the
    base for Inheritance by NumberCard and AnimalCard."""

    def __init__(self, symbol):
        self._symbol = symbol
        self._is_face_up = False
        self._is_matched = False

    @property
    def symbol(self):
        return self._symbol

    @property
    def is_face_up(self):
        return self._is_face_up

    @property
    def is_matched(self):
        return self._is_matched

    def flip(self):
        if not self._is_matched:
            self._is_face_up = not self._is_face_up

    def set_matched(self):
        self._is_matched = True
        self._is_face_up = True

    def reset(self):
        self._is_face_up = False
        self._is_matched = False

    def get_display(self):
        """Polymorphic: subclasses override to change how the symbol looks."""
        if self._is_face_up or self._is_matched:
            return str(self._symbol)
        return "?"


class NumberCard(Card):
    """Inherits from Card. Overrides get_display() — Polymorphism."""

    def get_display(self):
        if self._is_face_up or self._is_matched:
            return f"[ {self._symbol} ]"
        return "[ ? ]"


class AnimalCard(Card):
    """Inherits from Card. Overrides get_display() — Polymorphism."""

    def get_display(self):
        if self._is_face_up or self._is_matched:
            return self._symbol   # emoji character
        return "🂠"
