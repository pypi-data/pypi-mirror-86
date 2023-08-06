# Copyright (C) 2020 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later
import curses

from squirrelbattle.display.display import Box, Display


class MessageDisplay(Display):
    """
    Display a message in a popup.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.box = Box(fg_border_color=curses.COLOR_RED, *args, **kwargs)
        self.message = ""
        self.pad = self.newpad(1, 1)

    def update_message(self, msg: str) -> None:
        self.message = msg

    def display(self) -> None:
        self.box.refresh(self.y - 1, self.x - 2,
                         self.height + 2, self.width + 4)
        self.box.display()
        self.pad.erase()
        self.addstr(self.pad, 0, 0, self.message, curses.A_BOLD)
        self.refresh_pad(self.pad, 0, 0, self.y, self.x,
                         self.height + self.y - 1,
                         self.width + self.x - 1)
