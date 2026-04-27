import random
from models.card import NumberCard, AnimalCard
from assets.themes.numbers import NUMBER_SYMBOLS
from assets.themes.animals import ANIMAL_SYMBOLS

# card_count -> (rows, cols)
GRID_SIZES = {12: (3, 4), 16: (4, 4), 20: (4, 5)}


class Board:
    """Manages the card grid. Demonstrates Encapsulation — _cards is private
    and all access goes through public methods."""

    def __init__(self, card_count=16, theme="numbers"):
        if card_count not in GRID_SIZES:
            raise ValueError(f"card_count must be one of {list(GRID_SIZES)}")
        self._card_count = card_count
        self._theme = theme
        self._rows, self._cols = GRID_SIZES[card_count]
        self._cards = []
        self._build()

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    @property
    def card_count(self):
        return self._card_count

    def _build(self):
        pairs = self._card_count // 2
        if self._theme == "animals":
            symbols = ANIMAL_SYMBOLS[:pairs]
            card_cls = AnimalCard
        else:
            symbols = NUMBER_SYMBOLS[:pairs]
            card_cls = NumberCard
        cards = [card_cls(s) for s in symbols * 2]
        random.shuffle(cards)
        self._cards = cards

    def get_card(self, row, col):
        return self._cards[row * self._cols + col]

    def check_match(self, card1, card2):
        return card1.symbol == card2.symbol and card1 is not card2

    def is_complete(self):
        return all(c.is_matched for c in self._cards)

    def reset(self):
        self._build()

    def get_all_cards(self):
        return list(self._cards)
