import unittest
import sys
from pathlib import Path

# Add the project root so tests work with unittest discovery from this folder.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from enemy_ai import (
    Enemy, EnemyState, Grid, Player, manhattan_distance,
    shortest_path, update_enemy
)


class EnemyAITests(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(7, 5, walls={(3, 1), (3, 2), (3, 3)})

    def test_manhattan_distance(self):
        self.assertEqual(manhattan_distance((1, 1), (4, 3)), 5)

    def test_shortest_path_avoids_wall(self):
        path = shortest_path(self.grid, (1, 2), (5, 2))
        self.assertTrue(path)
        self.assertEqual(path[0], (1, 2))
        self.assertEqual(path[-1], (5, 2))
        self.assertTrue(all(p not in self.grid.walls for p in path))

    def test_unreachable_goal_returns_empty_path(self):
        blocked_grid = Grid(3, 3, walls={(1, 0), (1, 1), (1, 2)})
        self.assertEqual(shortest_path(blocked_grid, (0, 1), (2, 1)), [])

    def test_enemy_chases_player(self):
        enemy = Enemy((1, 2), detection_range=6)
        player = Player((5, 2))
        old_position = enemy.position
        update_enemy(enemy, player, self.grid)
        self.assertEqual(enemy.state, EnemyState.CHASE)
        self.assertNotEqual(enemy.position, old_position)

    def test_enemy_attacks_when_adjacent(self):
        enemy = Enemy((2, 2), attack_range=1, damage=15)
        player = Player((3, 2), health=100)
        update_enemy(enemy, player, self.grid)
        self.assertEqual(enemy.state, EnemyState.ATTACK)
        self.assertEqual(player.health, 85)

    def test_player_health_never_below_zero(self):
        enemy = Enemy((1, 1), attack_range=1, damage=200)
        player = Player((2, 1), health=20)
        update_enemy(enemy, player, self.grid)
        self.assertEqual(player.health, 0)

    def test_dead_enemy_does_not_attack(self):
        enemy = Enemy((1, 1), health=0, attack_range=2)
        player = Player((2, 1), health=100)
        update_enemy(enemy, player, self.grid)
        self.assertEqual(player.health, 100)

    def test_player_out_of_range_enemy_idles_without_memory(self):
        enemy = Enemy((0, 0), detection_range=1)
        player = Player((6, 4))
        update_enemy(enemy, player, self.grid)
        self.assertEqual(enemy.state, EnemyState.IDLE)


if __name__ == "__main__":
    unittest.main(verbosity=2)
