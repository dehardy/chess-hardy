# Chess Hardy

Chess Hardy is a local two-player chess application written in Python with Pygame. I built it independently in February 2022 as an early-career project to explore object-oriented design, board-state management, chess move generation, and event-driven user interfaces.

> **Historical project:** This repository preserves the original 2022 implementation. It represents an early stage of my development rather than my current engineering practices, and it is not a complete chess engine.

## Features

- An 8×8 chess board rendered with Pygame
- Standard starting positions and piece-specific movement
- Mouse-driven piece selection and move highlighting
- Alternating local turns, movement, and captures
- Basic obstruction, check, and checkmate logic

## Getting started

### Requirements

- Python 3
- Pygame

### Installation

```bash
git clone https://github.com/dehardy/chess-hardy.git
cd chess-hardy

python3 -m venv .venv
source .venv/bin/activate
python -m pip install pygame
```

On Windows, activate the virtual environment with:

```powershell
.\.venv\Scripts\activate
```

### Run the application

Run the game from the repository root so the sprite paths resolve correctly:

```bash
python chess_ui.py
```

White moves first. Click a piece belonging to the current player to highlight its candidate moves, then click a highlighted square to move it.

## Project structure

```text
chess-hardy/
├── chess_api.py     # Board state, pieces, move generation, and rule logic
├── chess_ui.py      # Pygame rendering, input handling, and turn management
└── sprites/         # Images for the black and white chess pieces
```

`chess_api.py` contains the board model and piece classes. `chess_ui.py` renders that state, handles mouse input, highlights candidate destinations, and advances turns.

## Known limitations

This version does not implement every chess rule or production safeguard:

- Castling, en passant, and pawn promotion are not implemented
- Stalemate and other draw conditions are not detected
- Move selection does not fully prevent a player from leaving their king in check
- Check and checkmate handling has unhandled edge cases
- There is no computer opponent, network play, persistence, or automated test suite
- Display behavior and sprite loading are coupled directly to the Pygame UI

## Status

This repository is preserved as a historical learning project and a record of how I approached my first independently designed application.
