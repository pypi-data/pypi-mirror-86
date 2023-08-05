from typing import Optional

from .player import Player
from ..interfaces import Entity, FightingEntity, Map


class Item(Entity):
    """
    A class for items
    """
    held: bool
    held_by: Optional[Player]

    def __init__(self, held: bool = False, held_by: Optional[Player] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.held = held
        self.held_by = held_by

    def drop(self, y: int, x: int) -> None:
        """
        The item is dropped from the inventory onto the floor
        """
        if self.held:
            self.held_by.inventory.remove(self)
            self.held = False
            self.held_by = None
        self.map.add_entity(self)
        self.move(y, x)

    def hold(self, player: "Player") -> None:
        """
        The item is taken from the floor and put into the inventory
        """
        self.held = True
        self.held_by = player
        self.map.remove_entity(self)
        player.inventory.append(self)

    def save_state(self) -> dict:
        """
        Saves the state of the entity into a dictionary
        """
        d = super().save_state()
        d["held"] = self.held
        return d


class Heart(Item):
    """
    A heart item to return health to the player
    """
    healing: int

    def __init__(self, healing: int = 5, *args, **kwargs):
        super().__init__(name="heart", *args, **kwargs)
        self.healing = healing

    def hold(self, player: "Player") -> None:
        """
        When holding a heart, heal the player and don't put item in inventory.
        """
        player.health = min(player.maxhealth, player.health + self.healing)
        self.map.remove_entity(self)

    def save_state(self) -> dict:
        """
        Saves the state of the header into a dictionary
        """
        d = super().save_state()
        d["healing"] = self.healing
        return d


class Bomb(Item):
    """
    A bomb item intended to deal damage to enemies at long range
    """
    damage: int = 5
    exploding: bool

    def __init__(self, damage: int = 5, exploding: bool = False,
                 *args, **kwargs):
        super().__init__(name="bomb", *args, **kwargs)
        self.damage = damage
        self.exploding = exploding

    def drop(self, x: int, y: int) -> None:
        super().drop(x, y)
        self.exploding = True

    def act(self, m: Map) -> None:
        """
        Special exploding action of the bomb
        """
        if self.exploding:
            for e in m.entities.copy():
                if abs(e.x - self.x) + abs(e.y - self.y) <= 1 and \
                        isinstance(e, FightingEntity):
                    e.take_damage(self, self.damage)

    def save_state(self) -> dict:
        """
        Saves the state of the bomb into a dictionary
        """
        d = super().save_state()
        d["exploding"] = self.exploding
        d["damage"] = self.damage
        return d
