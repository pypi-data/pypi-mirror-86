import curses
from typing import Any


class TexturePack:
    _packs = dict()

    name: str
    tile_width: int
    tile_fg_color: int
    tile_bg_color: int
    entity_fg_color: int
    entity_bg_color: int
    EMPTY: str
    WALL: str
    FLOOR: str
    PLAYER: str

    ASCII_PACK: "TexturePack"
    SQUIRREL_PACK: "TexturePack"

    def __init__(self, name: str, **kwargs):
        self.name = name
        self.__dict__.update(**kwargs)
        TexturePack._packs[name] = self

    def __getitem__(self, item: str) -> Any:
        return self.__dict__[item]

    @classmethod
    def get_pack(cls, name: str) -> "TexturePack":
        return cls._packs[name.lower()]

    @classmethod
    def get_next_pack_name(cls, name: str) -> str:
        return "squirrel" if name == "ascii" else "ascii"


TexturePack.ASCII_PACK = TexturePack(
    name="ascii",
    tile_width=1,
    tile_fg_color=curses.COLOR_WHITE,
    tile_bg_color=curses.COLOR_BLACK,
    entity_fg_color=curses.COLOR_WHITE,
    entity_bg_color=curses.COLOR_BLACK,
    EMPTY=' ',
    WALL='#',
    FLOOR='.',
    PLAYER='@',
    HEDGEHOG='*',
    HEART='❤',
    BOMB='o',
    RABBIT='Y',
    BEAVER='_',
    TEDDY_BEAR='8',
)

TexturePack.SQUIRREL_PACK = TexturePack(
    name="squirrel",
    tile_width=2,
    tile_fg_color=curses.COLOR_WHITE,
    tile_bg_color=curses.COLOR_BLACK,
    entity_fg_color=curses.COLOR_WHITE,
    entity_bg_color=curses.COLOR_WHITE,
    EMPTY='  ',
    WALL='🧱',
    FLOOR='██',
    PLAYER='🐿 ️',
    HEDGEHOG='🦔',
    HEART='💜',
    BOMB='💣',
    RABBIT='🐇',
    BEAVER='🦫',
    TEDDY_BEAR='🧸',
)
