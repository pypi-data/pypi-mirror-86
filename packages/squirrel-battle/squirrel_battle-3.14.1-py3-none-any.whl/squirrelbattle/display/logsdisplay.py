# Copyright (C) 2020 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

from squirrelbattle.display.display import Display
from squirrelbattle.interfaces import Logs


class LogsDisplay(Display):

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.pad = self.newpad(self.rows, self.cols)

    def update_logs(self, logs: Logs) -> None:
        self.logs = logs

    def display(self) -> None:
        messages = self.logs.messages[-self.height:]
        messages = messages[::-1]
        self.pad.erase()
        for i in range(min(self.height, len(messages))):
            self.addstr(self.pad, self.height - i - 1, self.x,
                        messages[i][:self.width])
        self.refresh_pad(self.pad, 0, 0, self.y, self.x,
                         self.y + self.height - 1, self.x + self.width - 1)
