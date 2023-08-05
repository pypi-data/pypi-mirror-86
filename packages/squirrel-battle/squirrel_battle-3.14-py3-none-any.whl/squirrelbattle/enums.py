from enum import Enum, auto
from typing import Optional

from squirrelbattle.settings import Settings

# This file contains a few useful enumeration classes used elsewhere in the code


class DisplayActions(Enum):
    """
    Display actions options for the callable displayaction Game uses
    It just calls the same action on the display object displayaction refers to.
    """
    REFRESH = auto()
    UPDATE = auto()


class GameMode(Enum):
    """
    Game mode options
    """
    MAINMENU = auto()
    PLAY = auto()
    SETTINGS = auto()
    INVENTORY = auto()


class KeyValues(Enum):
    """
    Key values options used in the game
    """
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    ENTER = auto()
    SPACE = auto()

    @staticmethod
    def translate_key(key: str, settings: Settings) -> Optional["KeyValues"]:
        """
        Translate the raw string key into an enum value that we can use.
        """
        if key in (settings.KEY_DOWN_SECONDARY,
                   settings.KEY_DOWN_PRIMARY):
            return KeyValues.DOWN
        elif key in (settings.KEY_LEFT_PRIMARY,
                     settings.KEY_LEFT_SECONDARY):
            return KeyValues.LEFT
        elif key in (settings.KEY_RIGHT_PRIMARY,
                     settings.KEY_RIGHT_SECONDARY):
            return KeyValues.RIGHT
        elif key in (settings.KEY_UP_PRIMARY,
                     settings.KEY_UP_SECONDARY):
            return KeyValues.UP
        elif key == settings.KEY_ENTER:
            return KeyValues.ENTER
        elif key == ' ':
            return KeyValues.SPACE
        return None
