import os
import unittest

from squirrelbattle.bootstrap import Bootstrap
from squirrelbattle.display.display import Display
from squirrelbattle.display.display_manager import DisplayManager
from squirrelbattle.entities.player import Player
from squirrelbattle.game import Game, KeyValues, GameMode
from squirrelbattle.menus import MainMenuValues
from squirrelbattle.settings import Settings


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        """
        Setup game.
        """
        self.game = Game()
        self.game.new_game()
        display = DisplayManager(None, self.game)
        self.game.display_actions = display.handle_display_action

    def test_load_game(self) -> None:
        """
        Save a game and reload it.
        """
        old_state = self.game.save_state()

        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertEqual(self.game.main_menu.validate(), MainMenuValues.SAVE)
        self.game.handle_key_pressed(KeyValues.ENTER)  # Save game
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertEqual(self.game.main_menu.validate(), MainMenuValues.LOAD)
        self.game.handle_key_pressed(KeyValues.ENTER)  # Load game

        new_state = self.game.save_state()
        self.assertEqual(old_state, new_state)

    def test_bootstrap_fail(self) -> None:
        """
        Ensure that the test can't play the game,
        because there is no associated shell.
        Yeah, that's only for coverage.
        """
        self.assertRaises(Exception, Bootstrap.run_game)
        self.assertEqual(os.getenv("TERM", "unknown"), "unknown")

    def test_key_translation(self) -> None:
        """
        Test key bindings.
        """
        self.game.settings = Settings()

        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_UP_PRIMARY, self.game.settings),
            KeyValues.UP)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_UP_SECONDARY, self.game.settings),
            KeyValues.UP)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_DOWN_PRIMARY, self.game.settings),
            KeyValues.DOWN)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_DOWN_SECONDARY, self.game.settings),
            KeyValues.DOWN)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_LEFT_PRIMARY, self.game.settings),
            KeyValues.LEFT)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_LEFT_SECONDARY, self.game.settings),
            KeyValues.LEFT)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_RIGHT_PRIMARY, self.game.settings),
            KeyValues.RIGHT)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_RIGHT_SECONDARY, self.game.settings),
            KeyValues.RIGHT)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_ENTER, self.game.settings),
            KeyValues.ENTER)
        self.assertEqual(KeyValues.translate_key(' ', self.game.settings),
                         KeyValues.SPACE)
        self.assertEqual(KeyValues.translate_key('plop', self.game.settings),
                         None)

    def test_key_press(self) -> None:
        """
        Press a key and see what is done.
        """
        self.assertEqual(self.game.state, GameMode.MAINMENU)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.START)
        self.game.handle_key_pressed(KeyValues.UP)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.START)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.RESUME)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.SAVE)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.LOAD)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.SETTINGS)
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertEqual(self.game.state, GameMode.SETTINGS)

        self.game.handle_key_pressed(KeyValues.SPACE)
        self.assertEqual(self.game.state, GameMode.MAINMENU)

        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.EXIT)
        self.assertRaises(SystemExit, self.game.handle_key_pressed,
                          KeyValues.ENTER)

        self.game.handle_key_pressed(KeyValues.UP)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.SETTINGS)
        self.game.handle_key_pressed(KeyValues.UP)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.LOAD)
        self.game.handle_key_pressed(KeyValues.UP)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.SAVE)
        self.game.handle_key_pressed(KeyValues.UP)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.RESUME)
        self.game.handle_key_pressed(KeyValues.UP)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.START)

        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertEqual(self.game.state, GameMode.PLAY)

        # Kill entities
        for entity in self.game.map.entities.copy():
            if not isinstance(entity, Player):
                self.game.map.remove_entity(entity)

        y, x = self.game.player.y, self.game.player.x
        self.game.handle_key_pressed(KeyValues.DOWN)
        new_y, new_x = self.game.player.y, self.game.player.x
        self.assertEqual(new_y, y + 1)
        self.assertEqual(new_x, x)

        y, x = new_y, new_x
        self.game.handle_key_pressed(KeyValues.RIGHT)
        new_y, new_x = self.game.player.y, self.game.player.x
        self.assertEqual(new_y, y)
        self.assertEqual(new_x, x + 1)

        y, x = self.game.player.y, self.game.player.x
        self.game.handle_key_pressed(KeyValues.UP)
        new_y, new_x = self.game.player.y, self.game.player.x
        self.assertEqual(new_y, y - 1)
        self.assertEqual(new_x, x)

        y, x = self.game.player.y, self.game.player.x
        self.game.handle_key_pressed(KeyValues.LEFT)
        new_y, new_x = self.game.player.y, self.game.player.x
        self.assertEqual(new_y, y)
        self.assertEqual(new_x, x - 1)

        self.game.handle_key_pressed(KeyValues.SPACE)
        self.assertEqual(self.game.state, GameMode.MAINMENU)

    def test_new_game(self) -> None:
        """
        Ensure that the start button starts a new game.
        """
        old_map = self.game.map
        old_player = self.game.player
        self.game.handle_key_pressed(KeyValues.ENTER)  # Start new game
        new_map = self.game.map
        new_player = self.game.player
        # Ensure that
        self.assertNotEqual(old_map, new_map)
        self.assertNotEqual(old_player, new_player)

        self.game.handle_key_pressed(KeyValues.SPACE)
        old_map = new_map
        old_player = new_player
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.ENTER)  # Resume game
        new_map = self.game.map
        new_player = self.game.player
        self.assertEqual(old_map, new_map)
        self.assertEqual(old_player, new_player)

    def test_settings_menu(self) -> None:
        """
        Ensure that the settings menu is working properly.
        """
        self.game.settings = Settings()

        # Open settings menu
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertEqual(self.game.state, GameMode.SETTINGS)

        # Define the "move up" key to 'w'
        self.assertFalse(self.game.settings_menu.waiting_for_key)
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertTrue(self.game.settings_menu.waiting_for_key)
        self.game.handle_key_pressed(None, 'w')
        self.assertFalse(self.game.settings_menu.waiting_for_key)
        self.assertEqual(self.game.settings.KEY_UP_PRIMARY, 'w')

        # Navigate to "move left"
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.UP)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)

        # Define the "move up" key to 'a'
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertTrue(self.game.settings_menu.waiting_for_key)
        # Can't used a mapped key
        self.game.handle_key_pressed(None, 's')
        self.assertTrue(self.game.settings_menu.waiting_for_key)
        self.game.handle_key_pressed(None, 'a')
        self.assertFalse(self.game.settings_menu.waiting_for_key)
        self.assertEqual(self.game.settings.KEY_LEFT_PRIMARY, 'a')

        # Navigate to "texture pack"
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)

        # Change texture pack
        self.assertEqual(self.game.settings.TEXTURE_PACK, "ascii")
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertEqual(self.game.settings.TEXTURE_PACK, "squirrel")
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertEqual(self.game.settings.TEXTURE_PACK, "ascii")

        # Navigate to "back" button
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)

        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertEqual(self.game.state, GameMode.MAINMENU)

    def test_dead_screen(self) -> None:
        """
        Kill player and render dead screen.
        """
        self.game.state = GameMode.PLAY
        # Kill player
        self.game.player.take_damage(self.game.player,
                                     self.game.player.health + 2)
        y, x = self.game.player.y, self.game.player.x
        for key in [KeyValues.UP, KeyValues.DOWN,
                    KeyValues.LEFT, KeyValues.RIGHT]:
            self.game.handle_key_pressed(key)
            new_y, new_x = self.game.player.y, self.game.player.x
            self.assertEqual(new_y, y)
            self.assertEqual(new_x, x)

    def test_not_implemented(self) -> None:
        """
        Check that some functions are not implemented, only for coverage.
        """
        self.assertRaises(NotImplementedError, Display.display, None)
