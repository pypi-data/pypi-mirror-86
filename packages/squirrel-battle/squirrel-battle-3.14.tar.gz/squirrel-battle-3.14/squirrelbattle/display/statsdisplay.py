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
        string = ""
        for _ in range(self.width - 1):
            string = string + "-"
        self.pad.addstr(0, 0, string)
        string2 = "Player -- LVL {}  EXP {}/{}  HP {}/{}"\
            .format(self.player.level, self.player.current_xp,
                    self.player.max_xp, self.player.health,
                    self.player.maxhealth)
        for _ in range(self.width - len(string2) - 1):
            string2 = string2 + " "
        self.pad.addstr(1, 0, string2)
        string3 = "Stats : STR {}  INT {}  CHR {}  DEX {} CON {}"\
            .format(self.player.strength,
                    self.player.intelligence, self.player.charisma,
                    self.player.dexterity, self.player.constitution)
        for _ in range(self.width - len(string3) - 1):
            string3 = string3 + " "
        self.pad.addstr(2, 0, string3)

        inventory_str = "Inventaire : " + "".join(
            self.pack[item.name.upper()] for item in self.player.inventory)
        self.pad.addstr(3, 0, inventory_str)

        if self.player.dead:
            self.pad.addstr(4, 0, "VOUS ÊTES MORT",
                            curses.A_BOLD | curses.A_BLINK | curses.A_STANDOUT
                            | self.color_pair(3))

    def display(self) -> None:
        self.pad.clear()
        self.update_pad()
        self.pad.refresh(0, 0, self.y, self.x,
                         4 + self.y, self.width + self.x)
