# Copyright (C) 2020 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

import curses
from squirrelbattle.display.display import VerticalSplit, HorizontalSplit
from squirrelbattle.display.mapdisplay import MapDisplay
from squirrelbattle.display.messagedisplay import MessageDisplay
from squirrelbattle.display.statsdisplay import StatsDisplay
from squirrelbattle.display.menudisplay import SettingsMenuDisplay, \
    MainMenuDisplay
from squirrelbattle.display.logsdisplay import LogsDisplay
from squirrelbattle.display.texturepack import TexturePack
from typing import Any
from squirrelbattle.game import Game, GameMode
from squirrelbattle.enums import DisplayActions


class DisplayManager:

    def __init__(self, screen: Any, g: Game):
        self.game = g
        self.screen = screen
        pack = TexturePack.get_pack(self.game.settings.TEXTURE_PACK)
        self.mapdisplay = MapDisplay(screen, pack)
        self.statsdisplay = StatsDisplay(screen, pack)
        self.mainmenudisplay = MainMenuDisplay(self.game.main_menu,
                                               screen, pack)
        self.settingsmenudisplay = SettingsMenuDisplay(screen, pack)
        self.logsdisplay = LogsDisplay(screen, pack)
        self.messagedisplay = MessageDisplay(screen=screen, pack=None)
        self.hbar = HorizontalSplit(screen, pack)
        self.vbar = VerticalSplit(screen, pack)
        self.displays = [self.statsdisplay, self.mapdisplay,
                         self.mainmenudisplay, self.settingsmenudisplay,
                         self.logsdisplay, self.messagedisplay]
        self.update_game_components()

    def handle_display_action(self, action: DisplayActions) -> None:
        if action == DisplayActions.REFRESH:
            self.refresh()
        elif action == DisplayActions.UPDATE:
            self.update_game_components()

    def update_game_components(self) -> None:
        for d in self.displays:
            d.pack = TexturePack.get_pack(self.game.settings.TEXTURE_PACK)
        self.mapdisplay.update_map(self.game.map)
        self.statsdisplay.update_player(self.game.player)
        self.settingsmenudisplay.update_menu(self.game.settings_menu)
        self.logsdisplay.update_logs(self.game.logs)
        self.messagedisplay.update_message(self.game.message)

    def refresh(self) -> None:
        if self.game.state == GameMode.PLAY:
            # The map pad has already the good size
            self.mapdisplay.refresh(0, 0, self.rows * 4 // 5,
                                    self.mapdisplay.pack.tile_width
                                    * (self.cols * 4 // 5
                                       // self.mapdisplay.pack.tile_width),
                                    resize_pad=False)
            self.statsdisplay.refresh(0, self.cols * 4 // 5 + 1,
                                      self.rows, self.cols // 5 - 1)
            self.logsdisplay.refresh(self.rows * 4 // 5 + 1, 0,
                                     self.rows // 5 - 1, self.cols * 4 // 5)
            self.hbar.refresh(self.rows * 4 // 5, 0, 1, self.cols * 4 // 5)
            self.vbar.refresh(0, self.cols * 4 // 5, self.rows, 1)
        if self.game.state == GameMode.MAINMENU:
            self.mainmenudisplay.refresh(0, 0, self.rows, self.cols)
        if self.game.state == GameMode.SETTINGS:
            self.settingsmenudisplay.refresh(0, 0, self.rows, self.cols - 1)

        if self.game.message:
            height, width = 0, 0
            for line in self.game.message.split("\n"):
                height += 1
                width = max(width, len(line))
            y, x = (self.rows - height) // 2, (self.cols - width) // 2
            self.messagedisplay.refresh(y, x, height, width)

        self.resize_window()

    def resize_window(self) -> bool:
        """
        If the window got resized, ensure that the screen size got updated.
        """
        y, x = self.screen.getmaxyx() if self.screen else (0, 0)
        if self.screen and curses.is_term_resized(self.rows,
                                                  self.cols):  # pragma: nocover
            curses.resizeterm(y, x)
            return True
        return False

    @property
    def rows(self) -> int:
        return curses.LINES if self.screen else 42

    @property
    def cols(self) -> int:
        return curses.COLS if self.screen else 42
