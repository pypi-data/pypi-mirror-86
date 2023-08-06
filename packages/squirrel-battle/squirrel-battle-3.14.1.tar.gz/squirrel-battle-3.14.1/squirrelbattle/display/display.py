# Copyright (C) 2020 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

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

    def truncate(self, msg: str, height: int, width: int) -> str:
        height = max(0, height)
        width = max(0, width)
        lines = msg.split("\n")
        lines = lines[:height]
        lines = [line[:width] for line in lines]
        return "\n".join(lines)

    def addstr(self, pad: Any, y: int, x: int, msg: str, *options) -> None:
        """
        Display a message onto the pad.
        If the message is too large, it is truncated vertically and horizontally
        """
        height, width = pad.getmaxyx()
        msg = self.truncate(msg, height - y, width - x - 1)
        if msg.replace("\n", "") and x >= 0 and y >= 0:
            return pad.addstr(y, x, msg, *options)

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
        if hasattr(self, "pad") and resize_pad and \
                self.height >= 0 and self.width >= 0:
            self.pad.resize(self.height + 1, self.width + 1)

    def refresh(self, *args, resize_pad: bool = True) -> None:
        if len(args) == 4:
            self.resize(*args, resize_pad)
        self.display()

    def refresh_pad(self, pad: Any, top_y: int, top_x: int,
                    window_y: int, window_x: int,
                    last_y: int, last_x: int) -> None:
        """
        Refresh a pad on a part of the window.
        The refresh starts at coordinates (top_y, top_x) from the pad,
        and is drawn from (window_y, window_x) to (last_y, last_x).
        If coordinates are invalid (negative indexes/length..., then nothing
        is drawn and no error is raised.
        """
        top_y, top_x = max(0, top_y), max(0, top_x)
        window_y, window_x = max(0, window_y), max(0, window_x)
        screen_max_y, screen_max_x = self.screen.getmaxyx() if self.screen \
            else (42, 42)
        last_y, last_x = min(screen_max_y - 1, last_y), \
            min(screen_max_x - 1, last_x)

        if last_y >= window_y and last_x >= window_x:
            # Refresh the pad only if coordinates are valid
            pad.refresh(top_y, top_x, window_y, window_x, last_y, last_x)

    def display(self) -> None:
        raise NotImplementedError

    @property
    def rows(self) -> int:
        return curses.LINES if self.screen else 42

    @property
    def cols(self) -> int:
        return curses.COLS if self.screen else 42


class VerticalSplit(Display):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pad = self.newpad(self.rows, 1)

    @property
    def width(self) -> int:
        return 1

    @width.setter
    def width(self, val: Any) -> None:
        pass

    def display(self) -> None:
        for i in range(self.height):
            self.addstr(self.pad, i, 0, "┃")
        self.refresh_pad(self.pad, 0, 0, self.y, self.x,
                         self.y + self.height - 1, self.x)


class HorizontalSplit(Display):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pad = self.newpad(1, self.cols)

    @property
    def height(self) -> int:
        return 1

    @height.setter
    def height(self, val: Any) -> None:
        pass

    def display(self) -> None:
        for i in range(self.width):
            self.addstr(self.pad, 0, i, "━")
        self.refresh_pad(self.pad, 0, 0, self.y, self.x, self.y,
                         self.x + self.width - 1)


class Box(Display):

    def __init__(self, *args, fg_border_color: Optional[int] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.pad = self.newpad(self.rows, self.cols)
        self.fg_border_color = fg_border_color or curses.COLOR_WHITE

        pair_number = 4 + self.fg_border_color
        self.init_pair(pair_number, self.fg_border_color, curses.COLOR_BLACK)
        self.pair = self.color_pair(pair_number)

    def display(self) -> None:
        self.addstr(self.pad, 0, 0, "┏" + "━" * (self.width - 2) + "┓",
                    self.pair)
        for i in range(1, self.height - 1):
            self.addstr(self.pad, i, 0, "┃", self.pair)
            self.addstr(self.pad, i, self.width - 1, "┃", self.pair)
        self.addstr(self.pad, self.height - 1, 0,
                    "┗" + "━" * (self.width - 2) + "┛", self.pair)
        self.refresh_pad(self.pad, 0, 0, self.y, self.x,
                         self.y + self.height - 1, self.x + self.width - 1)
