from enum import Enum
from typing import Any, Optional

from .display.texturepack import TexturePack
from .enums import GameMode, KeyValues, DisplayActions
from .settings import Settings


class Menu:
    """
    A Menu object is the logical representation of a menu in the game
    """
    values: list

    def __init__(self):
        self.position = 0

    def go_up(self) -> None:
        """
        Moves the pointer of the menu on the previous value
        """
        self.position = max(0, self.position - 1)

    def go_down(self) -> None:
        """
        Moves the pointer of the menu on the next value
        """
        self.position = min(len(self.values) - 1, self.position + 1)

    def validate(self) -> Any:
        """
        Selects the value that is pointed by the menu pointer
        """
        return self.values[self.position]


class MainMenuValues(Enum):
    """
    Values of the main menu
    """
    START = 'Nouvelle partie'
    RESUME = 'Continuer'
    SAVE = 'Sauvegarder'
    LOAD = 'Charger'
    SETTINGS = 'Paramètres'
    EXIT = 'Quitter'

    def __str__(self):
        return self.value


class MainMenu(Menu):
    """
    A special instance of a menu : the main menu
    """
    values = [e for e in MainMenuValues]


class SettingsMenu(Menu):
    """
    A special instance of a menu : the settings menu
    """
    waiting_for_key: bool = False

    def update_values(self, settings: Settings) -> None:
        self.values = list(settings.__dict__.items())
        self.values.append(("RETURN", ["", "Retour"]))

    def handle_key_pressed(self, key: Optional[KeyValues], raw_key: str,
                           game: Any) -> None:
        """
        In the setting menu, we van select a setting and change it
        """
        if not self.waiting_for_key:
            # Navigate normally through the menu.
            if key == KeyValues.SPACE or \
                    key == KeyValues.ENTER and \
                    self.position == len(self.values) - 1:
                # Go back
                game.display_actions(DisplayActions.UPDATE)
                game.state = GameMode.MAINMENU
            if key == KeyValues.DOWN:
                self.go_down()
            if key == KeyValues.UP:
                self.go_up()
            if key == KeyValues.ENTER and self.position < len(self.values) - 1:
                # Change a setting
                option = self.values[self.position][0]
                if option == "TEXTURE_PACK":
                    game.settings.TEXTURE_PACK = \
                        TexturePack.get_next_pack_name(
                            game.settings.TEXTURE_PACK)
                    game.settings.write_settings()
                    self.update_values(game.settings)
                else:
                    self.waiting_for_key = True
                    self.update_values(game.settings)
        else:
            option = self.values[self.position][0]
            # Don't use an already mapped key
            if any(getattr(game.settings, opt) == raw_key
                   for opt in game.settings.settings_keys if opt != option):
                return
            setattr(game.settings, option, raw_key)
            game.settings.write_settings()
            self.waiting_for_key = False
            self.update_values(game.settings)
