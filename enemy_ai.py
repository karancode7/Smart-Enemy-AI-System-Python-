"""
Smart Enemy AI System for a 2D grid-based game.
Python 3.9+; standard library only.

The module models enemy behaviour using a finite-state machine:
IDLE -> CHASE -> ATTACK, with SEARCH after losing sight of the player.
A* is intentionally not required for this small demonstration; breadth-first
search (BFS) finds a shortest path on an unweighted grid.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, List, Optional, Set, Tuple

Position = Tuple[int, int]


class EnemyState(str, Enum):
    IDLE = "idle"
    CHASE = "chase"
    ATTACK = "attack"
    SEARCH = "search"


@dataclass
class Grid:
    width: int
    height: int
    walls: Set[Position] = field(default_factory=set)

    def is_walkable(self, position: Position) -> bool:
        x, y = position
        return (0 <= x < self.width and 0 <= y < self.height
                and position not in self.walls)

    def neighbors(self, position: Position) -> Iterable[Position]:
        x, y = position
        # Fixed order makes behaviour and tests deterministic.
        for candidate in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if self.is_walkable(candidate):
                yield candidate


@dataclass
class Player:
    position: Position
    health: int = 100


@dataclass
class Enemy:
    position: Position
    detection_range: int = 5
    attack_range: int = 1
    damage: int = 10
    health: int = 50
    state: EnemyState = EnemyState.IDLE
    last_seen_player: Optional[Position] = None
    search_steps_remaining: int = 3

    def is_alive(self) -> bool:
        return self.health > 0


def manhattan_distance(a: Position, b: Position) -> int:
    """Return Manhattan distance between two grid cells."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def shortest_path(grid: Grid, start: Position, goal: Position) -> List[Position]:
    """
    Return a shortest path including start and goal.
    Return [] when the goal is unreachable or either endpoint is blocked.
    """
    if not grid.is_walkable(start) or not grid.is_walkable(goal):
        return []
    if start == goal:
        return [start]

    queue = deque([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for neighbor in grid.neighbors(current):
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)

    if goal not in parent:
        return []

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    return list(reversed(path))


def update_enemy(enemy: Enemy, player: Player, grid: Grid) -> str:
    """
    Update enemy by one game tick and return a human-readable event.
    One tick permits at most one cell of movement or one attack.
    """
    if not enemy.is_alive():
        return "Enemy is defeated."
    if player.health <= 0:
        enemy.state = EnemyState.IDLE
        return "Player is defeated; enemy returns to idle."

    distance = manhattan_distance(enemy.position, player.position)

    # Player detected: choose attack or chase.
    if distance <= enemy.detection_range:
        enemy.last_seen_player = player.position
        if distance <= enemy.attack_range:
            enemy.state = EnemyState.ATTACK
            player.health = max(0, player.health - enemy.damage)
            return f"Enemy attacks; player health is {player.health}."
        enemy.state = EnemyState.CHASE
        path = shortest_path(grid, enemy.position, player.position)
        if len(path) >= 2:
            enemy.position = path[1]
            return f"Enemy moves to {enemy.position}."
        return "Enemy cannot find a path to the player."

    # Player is outside detection range: search last known location briefly.
    if enemy.last_seen_player is not None and enemy.search_steps_remaining > 0:
        enemy.state = EnemyState.SEARCH
        path = shortest_path(grid, enemy.position, enemy.last_seen_player)
        if len(path) >= 2:
            enemy.position = path[1]
        enemy.search_steps_remaining -= 1
        return f"Enemy searches last known position; {enemy.search_steps_remaining} search steps remain."

    enemy.state = EnemyState.IDLE
    enemy.last_seen_player = None
    enemy.search_steps_remaining = 3
    return "Enemy is idle."


def run_demo() -> None:
    """Run a short deterministic simulation and print each tick."""
    grid = Grid(8, 6, walls={(3, 1), (3, 2), (3, 3)})
    player = Player((6, 2))
    enemy = Enemy((1, 2))
    print("SMART ENEMY AI DEMO")
    print(f"Start: enemy={enemy.position}, player={player.position}, player HP={player.health}")
    for tick in range(1, 9):
        event = update_enemy(enemy, player, grid)
        print(f"Tick {tick}: state={enemy.state.value:6} | {event}")
        if player.health <= 0:
            break


if __name__ == "__main__":
    run_demo()
