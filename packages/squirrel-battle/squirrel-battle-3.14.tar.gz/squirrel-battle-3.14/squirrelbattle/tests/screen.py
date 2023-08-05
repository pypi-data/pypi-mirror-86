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

    def clear(self) -> None:
        pass

    def resize(self, height: int, width: int) -> None:
        pass
