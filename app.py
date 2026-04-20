import uuid
from flask import Flask, jsonify, request, render_template

from models.board import Board
from models.player import HumanPlayer, AIPlayer
from models.game_mode import SoloMode, PvPMode, PvAIMode
from models.game_state import GameState, HighScoreTracker

app = Flask(__name__)
app.secret_key = "memory-game-secret-key"

_games = {}       # game_id -> { board, game_mode, game_state, mode }
_tracker = HighScoreTracker()


# ── Helpers ────────────────────────────────────────────────────────────────────

def _board_data(board):
    cards = []
    for r in range(board.rows):
        row = []
        for c in range(board.cols):
            card = board.get_card(r, c)
            row.append({
                "display": card.get_display() if (card.is_face_up or card.is_matched) else "",
                "is_face_up": card.is_face_up,
                "is_matched": card.is_matched,
                "row": r,
                "col": c,
            })
        cards.append(row)
    return {"cards": cards, "rows": board.rows, "cols": board.cols}


def _scores_data(game_mode):
    return [{"name": p.name, "score": p.score} for p in game_mode.players]


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/start", methods=["POST"])
def start_game():
    data = request.json
    mode       = data.get("mode", "solo")
    card_count = int(data.get("card_count", 16))
    theme      = data.get("theme", "numbers")
    name1      = (data.get("name1") or "Player 1").strip()
    name2      = (data.get("name2") or "Player 2").strip()

    board = Board(card_count, theme)

    if mode == "solo":
        game_mode = SoloMode(HumanPlayer(name1))
    elif mode == "pvp":
        game_mode = PvPMode(HumanPlayer(name1), HumanPlayer(name2))
    else:
        game_mode = PvAIMode(HumanPlayer(name1), AIPlayer("Computer"))

    game_state = GameState(board, game_mode)
    game_state.start()

    game_id = str(uuid.uuid4())
    _games[game_id] = {
        "board": board,
        "game_mode": game_mode,
        "game_state": game_state,
        "mode": mode,
    }

    return jsonify({
        "game_id": game_id,
        "board": _board_data(board),
        "current_player": game_mode.current_player.name,
        "scores": _scores_data(game_mode),
        "state": game_state.state.name,
        "is_ai_turn": game_mode.is_ai_turn(),
        "mode": mode,
    })


@app.route("/api/flip", methods=["POST"])
def flip_card():
    data    = request.json
    game    = _games.get(data.get("game_id"))
    if not game:
        return jsonify({"error": "Game not found"}), 404

    board      = game["board"]
    game_state = game["game_state"]
    game_mode  = game["game_mode"]
    card       = board.get_card(int(data["row"]), int(data["col"]))
    result     = game_state.handle_flip(card, int(data["row"]), int(data["col"]))

    return jsonify({
        "result": result,
        "board": _board_data(board),
        "current_player": game_mode.current_player.name,
        "scores": _scores_data(game_mode),
        "state": game_state.state.name,
    })


@app.route("/api/resolve", methods=["POST"])
def resolve():
    data  = request.json
    game  = _games.get(data.get("game_id"))
    if not game:
        return jsonify({"error": "Game not found"}), 404

    board      = game["board"]
    game_state = game["game_state"]
    game_mode  = game["game_mode"]
    mode       = game["mode"]
    result     = game_state.resolve()

    response = {
        "result": result,
        "board": _board_data(board),
        "current_player": game_mode.current_player.name,
        "scores": _scores_data(game_mode),
        "state": game_state.state.name,
        "is_ai_turn": game_mode.is_ai_turn(),
    }

    if game_state.state.name == "GAME_OVER":
        winner = game_mode.get_winner()
        response["winner"]       = winner.name
        response["winner_score"] = winner.score
        if isinstance(game_mode, SoloMode):
            response["turns"] = game_mode.turns
        _tracker.record_score(mode, winner.name, winner.score)

    return jsonify(response)


@app.route("/api/ai_turn", methods=["POST"])
def ai_turn():
    data  = request.json
    game  = _games.get(data.get("game_id"))
    if not game:
        return jsonify({"error": "Game not found"}), 404

    board      = game["board"]
    game_state = game["game_state"]
    game_mode  = game["game_mode"]
    mode       = game["mode"]
    ai         = game_mode.current_player

    pos1 = ai.choose_card(board, set())
    if not pos1:
        return jsonify({"error": "AI has no moves"}), 400
    card1 = board.get_card(pos1[0], pos1[1])
    ai.remember(pos1[0], pos1[1], card1.symbol)
    game_state.handle_flip(card1, pos1[0], pos1[1])

    idx1 = pos1[0] * board.cols + pos1[1]
    pos2 = ai.choose_card(board, {idx1})
    if not pos2:
        return jsonify({"error": "AI has no second move"}), 400
    card2 = board.get_card(pos2[0], pos2[1])
    ai.remember(pos2[0], pos2[1], card2.symbol)
    game_state.handle_flip(card2, pos2[0], pos2[1])

    result = game_state.resolve()

    response = {
        "pos1": list(pos1),
        "pos2": list(pos2),
        "result": result,
        "board": _board_data(board),
        "current_player": game_mode.current_player.name,
        "scores": _scores_data(game_mode),
        "state": game_state.state.name,
        "is_ai_turn": game_mode.is_ai_turn(),
    }

    if game_state.state.name == "GAME_OVER":
        winner = game_mode.get_winner()
        response["winner"]       = winner.name
        response["winner_score"] = winner.score
        if isinstance(game_mode, SoloMode):
            response["turns"] = game_mode.turns
        _tracker.record_score(mode, winner.name, winner.score)

    return jsonify(response)


@app.route("/api/reset", methods=["POST"])
def reset_game():
    data  = request.json
    game  = _games.get(data.get("game_id"))
    if not game:
        return jsonify({"error": "Game not found"}), 404

    board      = game["board"]
    game_mode  = game["game_mode"]
    game_state = game["game_state"]

    board.reset()
    game_mode.reset()
    for p in game_mode.players:
        if isinstance(p, AIPlayer):
            p.reset_memory()
    game_state.reset(board, game_mode)
    game_state.start()

    return jsonify({
        "game_id": data["game_id"],
        "board": _board_data(board),
        "current_player": game_mode.current_player.name,
        "scores": _scores_data(game_mode),
        "state": game_state.state.name,
        "is_ai_turn": game_mode.is_ai_turn(),
        "mode": game["mode"],
    })


if __name__ == "__main__":
    app.run(debug=True)
