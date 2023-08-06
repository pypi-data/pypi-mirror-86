# Copyright (C) 2020 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later
from json import JSONDecodeError
from random import randint
from typing import Any, Optional
import json
import os
import sys

from .entities.player import Player
from .enums import GameMode, KeyValues, DisplayActions
from .interfaces import Map, Logs
from .resources import ResourceManager
from .settings import Settings
from . import menus
from typing import Callable


class Game:
    """
    The game object controls all actions in the game.
    """
    map: Map
    player: Player
    # display_actions is a display interface set by the bootstrapper
    display_actions: Callable[[DisplayActions], None]

    def __init__(self) -> None:
        """
        Init the game.
        """
        self.state = GameMode.MAINMENU
        self.main_menu = menus.MainMenu()
        self.settings_menu = menus.SettingsMenu()
        self.settings = Settings()
        self.settings.load_settings()
        self.settings.write_settings()
        self.settings_menu.update_values(self.settings)
        self.logs = Logs()
        self.message = None

    def new_game(self) -> None:
        """
        Create a new game on the screen.
        """
        # TODO generate a new map procedurally
        self.map = Map.load(ResourceManager.get_asset_path("example_map_2.txt"))
        self.map.logs = self.logs
        self.logs.clear()
        self.player = Player()
        self.map.add_entity(self.player)
        self.player.move(self.map.start_y, self.map.start_x)
        self.map.spawn_random_entities(randint(3, 10))

    def run(self, screen: Any) -> None:
        """
        Main infinite loop.
        We wait for the player's action, then we do what that should be done
        when the given key gets pressed.
        """
        while True:  # pragma no cover
            screen.erase()
            screen.refresh()
            self.display_actions(DisplayActions.REFRESH)
            key = screen.getkey()
            self.handle_key_pressed(
                KeyValues.translate_key(key, self.settings), key)

    def handle_key_pressed(self, key: Optional[KeyValues], raw_key: str = '')\
            -> None:
        """
        Indicates what should be done when the given key is pressed,
        according to the current game state.
        """
        if self.message:
            self.message = None
            self.display_actions(DisplayActions.REFRESH)
            return

        if self.state == GameMode.PLAY:
            self.handle_key_pressed_play(key)
        elif self.state == GameMode.MAINMENU:
            self.handle_key_pressed_main_menu(key)
        elif self.state == GameMode.SETTINGS:
            self.settings_menu.handle_key_pressed(key, raw_key, self)
        self.display_actions(DisplayActions.REFRESH)

    def handle_key_pressed_play(self, key: KeyValues) -> None:
        """
        In play mode, arrows or zqsd move the main character.
        """
        if key == KeyValues.UP:
            if self.player.move_up():
                self.map.tick()
        elif key == KeyValues.DOWN:
            if self.player.move_down():
                self.map.tick()
        elif key == KeyValues.LEFT:
            if self.player.move_left():
                self.map.tick()
        elif key == KeyValues.RIGHT:
            if self.player.move_right():
                self.map.tick()
        elif key == KeyValues.SPACE:
            self.state = GameMode.MAINMENU

    def handle_key_pressed_main_menu(self, key: KeyValues) -> None:
        """
        In the main menu, we can navigate through options.
        """
        if key == KeyValues.DOWN:
            self.main_menu.go_down()
        if key == KeyValues.UP:
            self.main_menu.go_up()
        if key == KeyValues.ENTER:
            option = self.main_menu.validate()
            if option == menus.MainMenuValues.START:
                self.new_game()
                self.display_actions(DisplayActions.UPDATE)
                self.state = GameMode.PLAY
            if option == menus.MainMenuValues.RESUME:
                self.state = GameMode.PLAY
            elif option == menus.MainMenuValues.SAVE:
                self.save_game()
            elif option == menus.MainMenuValues.LOAD:
                self.load_game()
            elif option == menus.MainMenuValues.SETTINGS:
                self.state = GameMode.SETTINGS
            elif option == menus.MainMenuValues.EXIT:
                sys.exit(0)

    def save_state(self) -> dict:
        """
        Saves the game to a dictionary
        """
        return self.map.save_state()

    def load_state(self, d: dict) -> None:
        """
        Loads the game from a dictionary
        """
        try:
            self.map.load_state(d)
        except KeyError:
            self.message = "Some keys are missing in your save file.\n" \
                           "Your save seems to be corrupt. It got deleted."
            os.unlink(ResourceManager.get_config_path("save.json"))
            self.display_actions(DisplayActions.UPDATE)
            return

        players = self.map.find_entities(Player)
        if not players:
            self.message = "No player was found on this map!\n" \
                           "Maybe you died?"
            self.player.health = 0
            self.display_actions(DisplayActions.UPDATE)
            return

        self.player = players[0]
        self.display_actions(DisplayActions.UPDATE)

    def load_game(self) -> None:
        """
        Loads the game from a file
        """
        file_path = ResourceManager.get_config_path("save.json")
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                try:
                    state = json.loads(f.read())
                    self.load_state(state)
                except JSONDecodeError:
                    self.message = "The JSON file is not correct.\n" \
                                   "Your save seems corrupted. It got deleted."
                    os.unlink(file_path)
                    self.display_actions(DisplayActions.UPDATE)

    def save_game(self) -> None:
        """
        Saves the game to a file
        """
        with open(ResourceManager.get_config_path("save.json"), "w") as f:
            f.write(json.dumps(self.save_state()))
