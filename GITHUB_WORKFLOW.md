# GitHub Workflow Guide

## Week 1 — Direct Commits to `main`

The repo is bare this week, so both partners commit directly to `main`.

### Partner A
1. Clone the repo locally
2. Add the full project skeleton (all folders and empty `__init__.py` files)
3. Implement `models/card.py` — `Card`, `NumberCard`, `AnimalCard`
4. Commit and push directly to `main`

```bash
git add .
git commit -m "feat: add project skeleton and Card class hierarchy"
git push origin main
```

### Partner B
1. Clone or pull the latest `main`
2. Implement `models/player.py` — `Player`, `HumanPlayer`
3. Write `tests/test_card.py`
4. Push to a new branch and open a Pull Request to `main`

```bash
git checkout -b feature/player-model
git add models/player.py tests/test_card.py
git commit -m "feat: add Player base class, HumanPlayer, and card tests"
git push origin feature/player-model
# Then open a Pull Request on GitHub targeting main
```

---

## Week 2 Onward — Feature Branches → `dev` → `main`

Starting Week 2, **never commit directly to `main`**. All work flows through feature branches.

### Branch Layout

```
main        ← stable; updated once per week via PR from dev
  └── dev   ← integration branch; all features merge here first
        ├── feature/board-model          (Partner A)
        ├── feature/ai-player            (Partner B)
        ├── feature/card-widget          (Partner A)
        ├── feature/score-menu-views     (Partner B)
        ├── feature/game-controller      (Partner A)
        ├── feature/integration-testing  (Partner B)
        ├── feature/ai-mode-integration  (Partner A)
        ├── feature/ui-polish            (Partner B)
        └── feature/high-score-tracker   (Partner B)
```

### Step-by-Step: Starting a Feature Branch

```bash
# 1. Make sure dev is up to date
git checkout dev
git pull origin dev

# 2. Create your feature branch from dev
git checkout -b feature/your-feature-name

# 3. Work and commit (aim for 3–5 commits, not one giant commit)
git add <files>
git commit -m "feat: describe what you added"

# 4. Push and open a PR targeting dev (NOT main)
git push origin feature/your-feature-name
```

### Step-by-Step: Reviewing a Partner's PR

1. Open the Pull Request on GitHub
2. Read the changed files
3. Leave at least one comment — even just **"LGTM ✅"** counts
4. Approve and merge into `dev`
5. Delete the branch after merging (GitHub shows a button for this)

### Step-by-Step: Weekly Merge from `dev` to `main`

At the end of each week, once the milestone is stable:

```bash
git checkout main
git merge dev
git push origin main
```

Or open a PR from `dev` → `main` on GitHub and merge it there.

---

## Rules Summary

| Rule | Reason |
|---|---|
| Week 1 only: commit directly to `main` | Repo is empty — no base to branch from yet |
| Week 2+: always branch from `dev` | Keeps `main` stable for demos |
| Name branches `feature/<short-description>` | Clean branch list on GitHub |
| Target `dev` in all PRs (not `main`) | `dev` is the integration buffer |
| Other partner reviews every PR | Creates visible review history for the instructor |
| Delete merged branches on GitHub | Keeps the repo tidy; commit history stays on `dev` |
| 3–5 commits per branch (not one giant commit) | Shows active weekly progress on GitHub's contribution graph |

---

## Commit Message Convention

```
feat: add new feature or class
fix: fix a bug
test: add or update tests
docs: update README or comments
refactor: restructure code without changing behavior
```

**Examples:**
```
feat: add Board class with encapsulated card grid and shuffle logic
feat: add AIPlayer with memory-based choose_card and GameState state machine
fix: resolve card flip state not resetting after missed pair
test: add test_board coverage for all three grid sizes
docs: add README with OOP concept reference table
```

---

## Weekly Commit Schedule

| Week | Partner A branch | Partner B branch |
|---|---|---|
| 1 | direct to `main` | `feature/player-model` → PR to `main` |
| 2 | `feature/board-model` → PR to `dev` | `feature/ai-player` → PR to `dev` |
| 3 | `feature/card-widget` → PR to `dev` | `feature/score-menu-views` → PR to `dev` |
| 4 | `feature/game-controller` → PR to `dev` | `feature/integration-testing` → PR to `dev` |
| 5 | `feature/ai-mode-integration` → PR to `dev` | `feature/ui-polish` → PR to `dev` |
| 6 | docstrings + README, merge `dev` → `main` | `feature/high-score-tracker` → PR to `dev` |
