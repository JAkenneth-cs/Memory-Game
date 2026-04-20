"use strict";

// ── API helpers ────────────────────────────────────────────────────────────────
async function post(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return res.json();
}

// ── State ──────────────────────────────────────────────────────────────────────
let gameId  = null;
let locked  = false;
let curMode = "solo";

// ── Screen helpers ─────────────────────────────────────────────────────────────
function showScreen(id) {
  document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
  document.getElementById(id).classList.add("active");
}
function setStatus(msg) { document.getElementById("status").textContent = msg; }
function showModal()  { document.getElementById("modal").classList.remove("hidden"); }
function hideModal()  { document.getElementById("modal").classList.add("hidden"); }

// ── Menu ───────────────────────────────────────────────────────────────────────
document.querySelectorAll('input[name="mode"]').forEach(r =>
  r.addEventListener("change", () => {
    document.getElementById("name2").disabled = r.value !== "pvp";
  })
);

document.getElementById("start-btn").addEventListener("click", async () => {
  const mode  = document.querySelector('input[name="mode"]:checked').value;
  const count = parseInt(document.querySelector('input[name="count"]:checked').value);
  const theme = document.querySelector('input[name="theme"]:checked').value;
  const name1 = document.getElementById("name1").value.trim() || "Player 1";
  const name2 = document.getElementById("name2").value.trim() || "Player 2";

  const data = await post("/api/start", { mode, card_count: count, theme, name1, name2 });
  gameId  = data.game_id;
  curMode = mode;
  locked  = false;

  showScreen("game-screen");
  renderBoard(data.board);
  renderScoreboard(data);
  setStatus("");

  if (data.is_ai_turn) setTimeout(doAiTurn, 900);
});

// ── Game header buttons ────────────────────────────────────────────────────────
document.getElementById("menu-btn").addEventListener("click", () => showScreen("menu-screen"));

document.getElementById("restart-btn").addEventListener("click", async () => {
  if (!gameId) return;
  locked = true;
  const data = await post("/api/reset", { game_id: gameId });
  locked = false;
  renderBoard(data.board);
  renderScoreboard(data);
  setStatus("");
  if (data.is_ai_turn) setTimeout(doAiTurn, 900);
});

document.getElementById("play-again-btn").addEventListener("click", async () => {
  hideModal();
  if (!gameId) return;
  locked = true;
  const data = await post("/api/reset", { game_id: gameId });
  locked = false;
  renderBoard(data.board);
  renderScoreboard(data);
  setStatus("");
  if (data.is_ai_turn) setTimeout(doAiTurn, 900);
});

document.getElementById("to-menu-btn").addEventListener("click", () => {
  hideModal();
  showScreen("menu-screen");
});

// ── Card click ─────────────────────────────────────────────────────────────────
async function onCardClick(row, col) {
  if (locked) return;

  const data = await post("/api/flip", { game_id: gameId, row, col });
  if (data.result === "ignored" || data.result === "same_card") return;

  renderBoard(data.board);
  renderScoreboard(data);

  if (data.result === "flipped_second") {
    locked = true;
    setTimeout(resolveFlip, 800);
  }
}

async function resolveFlip() {
  const data = await post("/api/resolve", { game_id: gameId });
  renderBoard(data.board);
  renderScoreboard(data);
  locked = false;

  if (data.result === "match") {
    setStatus("Match! 🎉");
    setTimeout(() => setStatus(""), 1400);
  } else {
    setStatus("");
  }

  if (data.state === "GAME_OVER") { setTimeout(() => showGameOver(data), 400); return; }

  if (data.is_ai_turn) {
    locked = true;
    setStatus("Computer is thinking…");
    setTimeout(doAiTurn, 1000);
  }
}

// ── AI turn ────────────────────────────────────────────────────────────────────
async function doAiTurn() {
  const data = await post("/api/ai_turn", { game_id: gameId });
  renderBoard(data.board);
  renderScoreboard(data);
  locked = false;

  setStatus(data.result === "match" ? "Computer found a match! 🤖" : "Computer missed.");
  setTimeout(() => setStatus(""), 1400);

  if (data.state === "GAME_OVER") { setTimeout(() => showGameOver(data), 400); return; }
  if (data.is_ai_turn) { locked = true; setTimeout(doAiTurn, 1200); }
}

// ── Render ─────────────────────────────────────────────────────────────────────
function renderBoard(boardData) {
  const el = document.getElementById("board");
  el.style.gridTemplateColumns = `repeat(${boardData.cols}, 80px)`;
  el.innerHTML = "";

  boardData.cards.forEach(row =>
    row.forEach(cell => {
      const btn = document.createElement("button");
      btn.className = "card";
      btn.textContent = cell.display;

      if (cell.is_matched)       btn.classList.add("matched");
      else if (cell.is_face_up)  btn.classList.add("revealed");
      else {
        btn.classList.add("hidden");
        btn.addEventListener("click", () => onCardClick(cell.row, cell.col));
      }

      el.appendChild(btn);
    })
  );
}

function renderScoreboard(data) {
  const scores = data.scores.map(s => `${s.name}: ${s.score}`).join("&nbsp;&nbsp;|&nbsp;&nbsp;");
  let extra = "";
  if (curMode === "solo" && data.turns !== undefined) extra = `&nbsp;&nbsp;Turns: ${data.turns}`;
  document.getElementById("scoreboard").innerHTML =
    `<div class="turn">&#9654; ${data.current_player}</div>` +
    `<div class="score">${scores}${extra}</div>`;
}

function showGameOver(data) {
  let title, body;
  if (curMode === "solo") {
    title = `Well done, ${data.winner}!`;
    body  = `Matches: ${data.winner_score}\nTurns taken: ${data.turns ?? 0}`;
  } else {
    title = "Game Over!";
    body  = `🏆 Winner: ${data.winner}\n\n` +
            data.scores.map(s => `${s.name}: ${s.score}`).join("\n");
  }
  document.getElementById("modal-title").textContent = title;
  document.getElementById("modal-body").textContent  = body;
  showModal();
}
