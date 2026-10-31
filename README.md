# Smart Enemy AI System (Python)

## Overview
A small, runnable demonstration of enemy behaviour for a 2D grid-based game.
It uses a finite-state machine and breadth-first search (BFS) pathfinding.
The project uses only the Python standard library; no paid software or extra
packages are required.

## Features
- Detects the player within a configurable Manhattan-distance range.
- Chases the player using a shortest walkable grid path.
- Attacks when the player is within attack range.
- Searches the player's last known position for a limited number of ticks.
- Returns to idle when the player is no longer detectable.
- Prevents health values from becoming negative.
- Includes automated unit tests.

## Requirements
- Python 3.9 or later
- Windows, macOS, or Linux

## Run the demo
Open a terminal in this folder and run:

```bash
python enemy_ai.py
```

## Run tests
From this folder, run:

```bash
python -m unittest discover -s tests -v
```

## Project structure
```text
smart_enemy_ai/
  enemy_ai.py
  README.md
  tests/
    test_enemy_ai.py
```

## Main code sections
- `Grid`: stores map size and blocked cells.
- `Player`: stores player position and health.
- `Enemy`: stores enemy position, health, ranges, and current AI state.
- `shortest_path`: BFS pathfinding; returns the shortest path or an empty list.
- `update_enemy`: applies one AI decision per tick.
- `run_demo`: runs a short example simulation.

## Design decisions
BFS is suitable because each grid move has equal cost. The finite-state machine
keeps behaviour understandable and easy to test. A production game could use
A* for larger maps, line-of-sight checks, animation events, cooldown timers,
and a game-engine physics/collision system.

## Known limitations
This is a logic module, not a complete graphical game. It uses Manhattan
distance rather than field-of-view geometry. The search behaviour is deliberately
simple and does not include sound, multiple enemies, or dynamic obstacles.
