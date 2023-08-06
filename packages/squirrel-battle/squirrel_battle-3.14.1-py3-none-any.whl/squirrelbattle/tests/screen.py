# Copyright (C) 2020 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Tuple


class FakePad:
    """
    In order to run tests, we simulate a fake curses pad that accepts functions
    but does nothing with them.
    """
    def addstr(self, y: int, x: int, message: str, color: int = 0) -> None:
        pass

    def refresh(self, pminrow: int, pmincol: int, sminrow: int,
                smincol: int, smaxrow: int, smaxcol: int) -> None:
        pass

    def erase(self) -> None:
        pass

    def resize(self, height: int, width: int) -> None:
        pass

    def getmaxyx(self) -> Tuple[int, int]:
        return 42, 42
