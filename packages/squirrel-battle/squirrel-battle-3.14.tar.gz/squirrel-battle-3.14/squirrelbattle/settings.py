import json
import os
from typing import Any, Generator

from .resources import ResourceManager


class Settings:
    """
    This class stores the settings of the game.
    Settings can be get by using for example settings.TEXTURE_PACK directly.
    The comment can be get by using settings.get_comment('TEXTURE_PACK').
    We can define the setting by simply use settings.TEXTURE_PACK = 'new_key'
    """
    def __init__(self):
        self.KEY_UP_PRIMARY = \
            ['z', 'Touche principale pour aller vers le haut']
        self.KEY_UP_SECONDARY = \
            ['KEY_UP', 'Touche secondaire pour aller vers le haut']
        self.KEY_DOWN_PRIMARY = \
            ['s', 'Touche principale pour aller vers le bas']
        self.KEY_DOWN_SECONDARY = \
            ['KEY_DOWN', 'Touche secondaire pour aller vers le bas']
        self.KEY_LEFT_PRIMARY = \
            ['q', 'Touche principale pour aller vers la gauche']
        self.KEY_LEFT_SECONDARY = \
            ['KEY_LEFT', 'Touche secondaire pour aller vers la gauche']
        self.KEY_RIGHT_PRIMARY = \
            ['d', 'Touche principale pour aller vers la droite']
        self.KEY_RIGHT_SECONDARY = \
            ['KEY_RIGHT', 'Touche secondaire pour aller vers la droite']
        self.KEY_ENTER = \
            ['\n', 'Touche pour valider un menu']
        self.TEXTURE_PACK = ['ascii', 'Pack de textures utilisé']

    def __getattribute__(self, item: str) -> Any:
        superattribute = super().__getattribute__(item)
        if item.isupper() and item in self.settings_keys:
            return superattribute[0]
        return superattribute

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.settings_keys:
            object.__getattribute__(self, name)[0] = value
            return
        return super().__setattr__(name, value)

    def get_comment(self, item: str) -> str:
        """
        Retrieve the comment of a setting.
        """
        if item in self.settings_keys:
            return object.__getattribute__(self, item)[1]
        for key in self.settings_keys:
            if getattr(self, key) == item:
                return object.__getattribute__(self, key)[1]

    @property
    def settings_keys(self) -> Generator[str, Any, None]:
        """
        Get the list of all parameters.
        """
        return (key for key in self.__dict__)

    def loads_from_string(self, json_str: str) -> None:
        """
        Dump settings
        """
        d = json.loads(json_str)
        for key in d:
            setattr(self, key, d[key])

    def dumps_to_string(self) -> str:
        """
        Dump settings
        """
        d = dict()
        for key in self.settings_keys:
            d[key] = getattr(self, key)
        return json.dumps(d, indent=4)

    def load_settings(self) -> None:
        """
        Loads the settings from a file
        """
        file_path = ResourceManager.get_config_path("settings.json")
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                self.loads_from_string(f.read())

    def write_settings(self) -> None:
        """
        Dumps the settings into a file
        """
        with open(ResourceManager.get_config_path("settings.json"), "w") as f:
            f.write(self.dumps_to_string())
