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
        self.assertEqual(len(self.game.blocks), 11)
        self.assertEqual(len(self.game.solids), 5)
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

    def test_character_input_activates_right_magnet(self) -> None:
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_o, unicode="o")
        self.game._remember_key(event, pressed=True)
        self.game.update(1 / 60)
        self.assertIn("o", self.game.held_keys)
        self.assertTrue(self.game.player.active_beams)
        self.assertEqual(self.game.player.active_beams[0].side, "right")

    def test_right_magnet_moves_the_bridge_instead_of_the_player(self) -> None:
        bridge = self.game.blocks[0]
        player_x = self.game.player.rect.x
        self.game.held_keys.add("p")
        self.game.update(1 / 60)
        self.assertIs(self.game.player.active_beams[0].target, bridge)
        self.assertEqual(self.game.player.active_beams[0].side, "right")
        self.assertGreater(bridge.velocity.x, 0)
        self.assertEqual(self.game.player.rect.x, player_x)
        for _ in range(120):
            self.game.update(1 / 60)
        self.assertGreaterEqual(bridge.rect.x, 500)

    def test_left_controls_move_an_object_on_the_left(self) -> None:
        bridge = self.game.blocks[0]
        bridge.rect.x = 60
        self.game.held_keys = {"j"}
        self.game.update(1 / 60)
        self.assertEqual(self.game.player.active_beams[0].side, "left")
        self.assertGreater(bridge.velocity.x, 0)

    def test_every_metallic_level_element_is_movable(self) -> None:
        self.assertFalse(any(solid.metal for solid in self.game.solids))
        self.assertTrue(all(hasattr(block, "velocity") for block in self.game.blocks))


if __name__ == "__main__":
    unittest.main()
