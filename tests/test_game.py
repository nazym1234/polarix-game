"""Tests rapides du prototype sans ouvrir de fenêtre."""

import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from src.game import Game


class GameSmokeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game()

    def tearDown(self) -> None:
        pygame.quit()

    def test_first_level_contains_expected_elements(self) -> None:
        self.assertEqual(len(self.game.cells), 2)
        self.assertEqual(len(self.game.blocks), 2)
        self.assertGreater(len(self.game.solids), 10)
        self.assertEqual(self.game.collected_cells, 0)

    def test_generator_requires_both_cells(self) -> None:
        self.game.player.rect.x = 2550
        self.game.activate_generator()
        self.assertFalse(self.game.finished)

        for cell in self.game.cells:
            cell.collected = True
        self.game.activate_generator()
        self.assertTrue(self.game.finished)

    def test_update_and_draw_complete_without_error(self) -> None:
        self.game.update(1 / 60)
        self.game.draw()
        self.assertEqual(self.game.screen.get_size(), (1280, 720))


if __name__ == "__main__":
    unittest.main()
