from random import choice

from .player import Player
from ..interfaces import FightingEntity, Map


class Monster(FightingEntity):
    """
    The class for all monsters in the dungeon.
    A monster must override this class, and the parameters are given
    in the __init__ function.
    An example of the specification of a monster that has a strength of 4
    and 20 max HP:

    class MyMonster(Monster):
        def __init__(self, strength: int = 4, maxhealth: int = 20,
                     *args, **kwargs) -> None:
            super().__init__(name="my_monster", strength=strength,
                             maxhealth=maxhealth, *args, **kwargs)

    With that way, attributes can be overwritten when the entity got created.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def act(self, m: Map) -> None:
        """
        By default, a monster will move randomly where it is possible
        And if a player is close to the monster, the monster run on the player.
        """
        target = None
        for entity in m.entities:
            if self.distance_squared(entity) <= 25 and \
                    isinstance(entity, Player):
                target = entity
                break

        # A Dijkstra algorithm has ran that targets the player.
        # With that way, monsters can simply follow the path.
        # If they can't move and they are already close to the player,
        # They hit.
        if target and (self.y, self.x) in target.paths:
            # Move to target player
            next_y, next_x = target.paths[(self.y, self.x)]
            moved = self.check_move(next_y, next_x, True)
            if not moved and self.distance_squared(target) <= 1:
                self.hit(target)
        else:
            for _ in range(100):
                if choice([self.move_up, self.move_down,
                          self.move_left, self.move_right])():
                    break


class Beaver(Monster):
    """
    A beaver monster
    """
    def __init__(self, strength: int = 2, maxhealth: int = 20,
                 *args, **kwargs) -> None:
        super().__init__(name="beaver", strength=strength,
                         maxhealth=maxhealth, *args, **kwargs)


class Hedgehog(Monster):
    """
    A really mean hedgehog monster
    """
    def __init__(self, strength: int = 3, maxhealth: int = 10,
                 *args, **kwargs) -> None:
        super().__init__(name="hedgehog", strength=strength,
                         maxhealth=maxhealth, *args, **kwargs)


class Rabbit(Monster):
    """
    A rabbit monster
    """
    def __init__(self, strength: int = 1, maxhealth: int = 15,
                 *args, **kwargs) -> None:
        super().__init__(name="rabbit", strength=strength,
                         maxhealth=maxhealth, *args, **kwargs)


class TeddyBear(Monster):
    """
    A cute teddybear monster
    """
    def __init__(self, strength: int = 0, maxhealth: int = 50,
                 *args, **kwargs) -> None:
        super().__init__(name="teddy_bear", strength=strength,
                         maxhealth=maxhealth, *args, **kwargs)
