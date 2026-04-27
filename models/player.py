class AIPlayer(Player):
    """Inherits from Player. Overrides choose_card() with memory-based logic."""

    def __init__(self, name="Computer"):
        super().__init__(name)
        self._memory = {}   # symbol -> list of (row, col)

    def remember(self, row, col, symbol):
        """Store a card position seen during a turn."""
        positions = self._memory.setdefault(symbol, [])
        if (row, col) not in positions:
            positions.append((row, col))

    def choose_card(self, board, flipped_indices):
        """Return (row, col) of the best card to flip.

        If the first card is already flipped and a matching position is known
        in memory, return that position. Otherwise pick a random unflipped card.
        """
        # If one card is already flipped, look for its match in memory
        if len(flipped_indices) == 1:
            first_idx = next(iter(flipped_indices))
            first_row, first_col = first_idx // board.cols, first_idx % board.cols
            first_card = board.get_card(first_row, first_col)
            known = self._memory.get(first_card.symbol, [])
            for pos in known:
                idx = pos[0] * board.cols + pos[1]
                if idx not in flipped_indices and not board.get_card(*pos).is_matched:
                    return pos

        # Look for any known pair we can complete on the first flip
        if not flipped_indices:
            for symbol, positions in self._memory.items():
                unmatched = [
                    p for p in positions
                    if not board.get_card(p[0], p[1]).is_matched
                    and (p[0] * board.cols + p[1]) not in flipped_indices
                ]
                if len(unmatched) >= 2:
                    return unmatched[0]

        # Fall back to a random unflipped, unmatched card
        candidates = [
            (r, c)
            for r in range(board.rows)
            for c in range(board.cols)
            if not board.get_card(r, c).is_matched
            and (r * board.cols + c) not in flipped_indices
        ]
        return random.choice(candidates) if candidates else None

    def reset_memory(self):
        self._memory = {}