import curses
from typing import Any, Optional, Union

from squirrelbattle.display.texturepack import TexturePack
from squirrelbattle.tests.screen import FakePad


class Display:
    x: int
    y: int
    width: int
    height: int
    pad: Any

    def __init__(self, screen: Any, pack: Optional[TexturePack] = None):
        self.screen = screen
        self.pack = pack or TexturePack.get_pack("ascii")

    def newpad(self, height: int, width: int) -> Union[FakePad, Any]:
        return curses.newpad(height, width) if self.screen else FakePad()

    def init_pair(self, number: int, foreground: int, background: int) -> None:
        return curses.init_pair(number, foreground, background) \
            if self.screen else None

    def color_pair(self, number: int) -> int:
        return curses.color_pair(number) if self.screen else 0

    def resize(self, y: int, x: int, height: int, width: int,
               resize_pad: bool = True) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if hasattr(self, "pad") and resize_pad:
            self.pad.resize(self.height - 1, self.width - 1)

    def refresh(self, *args, resize_pad: bool = True) -> None:
        if len(args) == 4:
            self.resize(*args, resize_pad)
        self.display()

    def display(self) -> None:
        raise NotImplementedError

    @property
    def rows(self) -> int:
        return curses.LINES if self.screen else 42

    @property
    def cols(self) -> int:
        return curses.COLS if self.screen else 42
