from squirrelbattle.game import Game
from squirrelbattle.display.display_manager import DisplayManager
from squirrelbattle.term_manager import TermManager


class Bootstrap:
    """
    The bootstrap object is used to bootstrap the game so that it starts
    properly.
    (It was initially created to avoid circular imports between the Game and
    Display classes)
    """

    @staticmethod
    def run_game():
        with TermManager() as term_manager:  # pragma: no cover
            game = Game()
            game.new_game()
            display = DisplayManager(term_manager.screen, game)
            game.display_actions = display.handle_display_action
            game.run(term_manager.screen)
