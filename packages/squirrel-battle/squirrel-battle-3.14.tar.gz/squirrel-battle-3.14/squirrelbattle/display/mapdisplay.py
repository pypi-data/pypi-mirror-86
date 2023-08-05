#!/usr/bin/env python
from squirrelbattle.interfaces import Map
from .display import Display


class MapDisplay(Display):

    def __init__(self, *args):
        super().__init__(*args)

    def update_map(self, m: Map) -> None:
        self.map = m
        self.pad = self.newpad(m.height, self.pack.tile_width * m.width + 1)

    def update_pad(self) -> None:
        self.init_pair(1, self.pack.tile_fg_color, self.pack.tile_bg_color)
        self.init_pair(2, self.pack.entity_fg_color, self.pack.entity_bg_color)
        self.pad.addstr(0, 0, self.map.draw_string(self.pack),
                        self.color_pair(1))
        for e in self.map.entities:
            self.pad.addstr(e.y, self.pack.tile_width * e.x,
                            self.pack[e.name.upper()], self.color_pair(2))

    def display(self) -> None:
        y, x = self.map.currenty, self.pack.tile_width * self.map.currentx
        deltay, deltax = (self.height // 2) + 1, (self.width // 2) + 1
        pminrow, pmincol = y - deltay, x - deltax
        sminrow, smincol = max(-pminrow, 0), max(-pmincol, 0)
        deltay, deltax = self.height - deltay, self.width - deltax
        smaxrow = self.map.height - (y + deltay) + self.height - 1
        smaxrow = min(smaxrow, self.height - 1)
        smaxcol = self.pack.tile_width * self.map.width - \
            (x + deltax) + self.width - 1
        smaxcol = min(smaxcol, self.width - 1)
        pminrow = max(0, min(self.map.height, pminrow))
        pmincol = max(0, min(self.pack.tile_width * self.map.width, pmincol))
        self.pad.clear()
        self.update_pad()
        self.pad.refresh(pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol)
