# Copyright (C) 2020 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

import curses

from .display import Display

from squirrelbattle.entities.player import Player


class StatsDisplay(Display):
    player: Player

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pad = self.newpad(self.rows, self.cols)
        self.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    def update_player(self, p: Player) -> None:
        self.player = p

    def update_pad(self) -> None:
        string2 = "Player -- LVL {}\nEXP {}/{}\nHP {}/{}"\
            .format(self.player.level, self.player.current_xp,
                    self.player.max_xp, self.player.health,
                    self.player.maxhealth)
        self.addstr(self.pad, 0, 0, string2)
        string3 = "STR {}\nINT {}\nCHR {}\nDEX {}\nCON {}"\
            .format(self.player.strength,
                    self.player.intelligence, self.player.charisma,
                    self.player.dexterity, self.player.constitution)
        self.addstr(self.pad, 3, 0, string3)

        inventory_str = "Inventaire : " + "".join(
            self.pack[item.name.upper()] for item in self.player.inventory)
        self.addstr(self.pad, 8, 0, inventory_str)

        if self.player.dead:
            self.addstr(self.pad, 10, 0, "VOUS ÊTES MORT",
                        curses.A_BOLD | curses.A_BLINK | curses.A_STANDOUT
                        | self.color_pair(3))

    def display(self) -> None:
        self.pad.erase()
        self.update_pad()
        self.refresh_pad(self.pad, 0, 0, self.y, self.x,
                         self.y + self.height - 1, self.width + self.x - 1)
