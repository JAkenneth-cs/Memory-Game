# Memory Game

A card-matching Memory Game built with **Python** and **tkinter**, developed as a Final Project to demonstrate all four Object-Oriented Programming (OOP) pillars.

---

## Owners
- Agbon | Velasco

## Features

- **3 Game Modes** — 1 Player (Solo), Human vs Human, Human vs AI
- **3 Card Counts** — 12 cards (3×4), 16 cards (4×4), 20 cards (4×5)
- **2 Themes** — Numbers and Animals (emoji)
- AI opponent with memory-based card selection
- Score tracking per player
- Play Again without restarting the window
- High score persistence (saved to `scores.json`)

---

## How to Run

**Requirements:** Python 3.10+ with tkinter (included in standard CPython installers)

```bash
# Clone the repository
git clone https://github.com/JAkenneth-cs/Memory-Game.git
cd Memory-Game

# Run the game
python main.py
```

**Run the tests:**
```bash
python -m pytest tests/
```

> No third-party packages needed — only Python's standard library is used.

---

## OOP Concepts

| Concept | Where | Example |
|---|---|---|
| **Classes & Objects** | All files | `Card`, `Board`, `Player`, `GameState`, `GameMode` — every class is instantiated as an object |
| **Encapsulation** | `models/card.py`, `models/board.py`, `models/player.py`, `models/game_state.py` | Private attributes (`_symbol`, `_cards`, `_score`, `_state`) exposed only through `@property` accessors and public methods |
| **Inheritance** | `models/card.py`, `models/player.py`, `models/game_mode.py`, `views/*.py` | `NumberCard` and `AnimalCard` extend `Card`; `HumanPlayer` and `AIPlayer` extend `Player`; `SoloMode`, `PvPMode`, `PvAIMode` extend `GameMode`; all views extend `tk.Frame` |
| **Polymorphism** | `views/board_view.py`, `controllers/game_controller.py` | `BoardView` calls `card.get_display()` on a mixed list of card types without `isinstance` checks; `GameController` calls `player.choose_card()` and `game_mode.on_match()` / `on_miss()` without knowing the concrete subtype |

---

## Project Structure

```
Memory-Game/
├── main.py                        # Entry point
├── models/
│   ├── card.py                    # Card, NumberCard, AnimalCard
│   ├── board.py                   # Board (supports 12 / 16 / 20 cards)
│   ├── player.py                  # Player, HumanPlayer, AIPlayer
│   ├── game_mode.py               # SoloMode, PvPMode, PvAIMode
│   └── game_state.py              # GameState (state machine) + HighScoreTracker
├── views/
│   ├── card_widget.py             # CardWidget — single card button
│   ├── board_view.py              # BoardView — full card grid
│   ├── scoreboard_view.py         # ScoreboardView — scores and turn info
│   └── menu_view.py               # MenuView — start screen and options
├── controllers/
│   └── game_controller.py         # Connects models to views
├── assets/themes/
│   ├── numbers.py                 # Number symbol set
│   └── animals.py                 # Animal emoji symbol set
├── tests/
│   ├── test_card.py
│   ├── test_board.py
│   ├── test_player.py
│   └── test_game_state.py
├── GITHUB_WORKFLOW.md             # Branch and commit guide for both partners
├── .gitignore
└── requirements.txt
```

---

## Class Hierarchy

```
Card ──────────────── NumberCard
                 └─── AnimalCard

Player ────────────── HumanPlayer
                 └─── AIPlayer

GameMode ─────────── SoloMode
                 ├─── PvPMode
                 └─── PvAIMode

tk.Frame ─────────── CardWidget
                 ├─── BoardView
                 ├─── ScoreboardView
                 └─── MenuView
```

---

## Contributors

| Partner | GitHub | Role |
|---|---|---|
| Partner A | [@JAkenneth-cs](https://github.com/JAkenneth-cs) | Card models, Board, Views, Game Controller |
| Partner B | *(add GitHub username)* | Player models, Game Modes, AI, Tests |

---

## Weekly Progress

| Week | Milestone |
|---|---|
| 1 | Project skeleton, `Card` hierarchy, `Player` base class |
| 2 | `Board` (all grid sizes), `AIPlayer`, `GameState`, `GameMode` classes |
| 3 | `CardWidget`, `BoardView`, `ScoreboardView`, `MenuView` |
| 4 | `GameController`, full integration, end-to-end playable game |
| 5 | AI mode, all card counts, Play Again, UI polish |
| 6 | High score tracker, docstrings, final merge to `main` |
