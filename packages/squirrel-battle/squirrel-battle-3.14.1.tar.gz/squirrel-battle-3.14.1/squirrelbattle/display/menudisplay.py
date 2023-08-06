# Copyright (C) 2020 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List

from squirrelbattle.menus import Menu, MainMenu
from .display import Display, Box
from ..resources import ResourceManager


class MenuDisplay(Display):
    position: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menubox = Box(*args, **kwargs)

    def update_menu(self, menu: Menu) -> None:
        self.menu = menu
        self.trueheight = len(self.values)
        self.truewidth = max([len(a) for a in self.values])

        # Menu values are printed in pad
        self.pad = self.newpad(self.trueheight, self.truewidth + 2)
        for i in range(self.trueheight):
            self.addstr(self.pad, i, 0, "  " + self.values[i])

    def update_pad(self) -> None:
        for i in range(self.trueheight):
            self.addstr(self.pad, i, 0, "  " + self.values[i])
        # set a marker on the selected line
        self.addstr(self.pad, self.menu.position, 0, ">")

    def display(self) -> None:
        cornery = 0 if self.height - 2 >= self.menu.position - 1 \
            else self.trueheight - self.height + 2 \
            if self.height - 2 >= self.trueheight - self.menu.position else 0

        # Menu box
        self.menubox.refresh(self.y, self.x, self.height, self.width)
        self.pad.erase()
        self.update_pad()
        self.refresh_pad(self.pad, cornery, 0, self.y + 1, self.x + 2,
                         self.height - 2 + self.y,
                         self.width - 2 + self.x)

    @property
    def preferred_width(self) -> int:
        return self.truewidth + 6

    @property
    def preferred_height(self) -> int:
        return self.trueheight + 2

    @property
    def values(self) -> List[str]:
        return [str(a) for a in self.menu.values]


class SettingsMenuDisplay(MenuDisplay):
    @property
    def values(self) -> List[str]:
        return [a[1][1] + (" : "
                + ("?" if self.menu.waiting_for_key
                    and a == self.menu.validate() else a[1][0])
            if a[1][0] else "") for a in self.menu.values]


class MainMenuDisplay(Display):
    def __init__(self, menu: MainMenu, *args):
        super().__init__(*args)
        self.menu = menu

        with open(ResourceManager.get_asset_path("ascii_art.txt"), "r") as file:
            self.title = file.read().split("\n")

        self.pad = self.newpad(max(self.rows, len(self.title) + 30),
                               max(len(self.title[0]) + 5, self.cols))

        self.menudisplay = MenuDisplay(self.screen, self.pack)
        self.menudisplay.update_menu(self.menu)

    def display(self) -> None:
        for i in range(len(self.title)):
            self.addstr(self.pad, 4 + i, max(self.width // 2
                        - len(self.title[0]) // 2 - 1, 0), self.title[i])
        self.refresh_pad(self.pad, 0, 0, self.y, self.x,
                         self.height + self.y - 1,
                         self.width + self.x - 1)
        menuwidth = min(self.menudisplay.preferred_width, self.width)
        menuy, menux = len(self.title) + 8, self.width // 2 - menuwidth // 2 - 1
        self.menudisplay.refresh(
            menuy, menux, min(self.menudisplay.preferred_height,
                              self.height - menuy), menuwidth)
