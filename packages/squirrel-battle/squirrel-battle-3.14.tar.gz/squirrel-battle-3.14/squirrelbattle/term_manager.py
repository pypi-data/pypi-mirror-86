import curses
from types import TracebackType


class TermManager:  # pragma: no cover
    """
    The TermManager object initializes the terminal, returns a screen object and
    de-initializes the terminal after use
    """
    def __init__(self):
        self.screen = curses.initscr()
        # convert escapes sequences to curses abstraction
        self.screen.keypad(True)
        # stop printing typed keys to the terminal
        curses.noecho()
        # send keys through without having to press <enter>
        curses.cbreak()
        # make cursor invisible
        curses.curs_set(False)
        # Enable colors
        curses.start_color()

    def __enter__(self):
        return self

    def __exit__(self, exc_type: type, exc_value: Exception,
                 exc_traceback: TracebackType) -> None:
        # restore the terminal to its original state
        self.screen.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.curs_set(True)
        curses.endwin()
