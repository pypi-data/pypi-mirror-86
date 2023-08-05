from random import randint
from typing import Dict, Tuple

from ..interfaces import FightingEntity


class Player(FightingEntity):
    """
    The class of the player
    """
    current_xp: int = 0
    max_xp: int = 10
    inventory: list
    paths: Dict[Tuple[int, int], Tuple[int, int]]

    def __init__(self, maxhealth: int = 20, strength: int = 5,
                 intelligence: int = 1, charisma: int = 1, dexterity: int = 1,
                 constitution: int = 1, level: int = 1, current_xp: int = 0,
                 max_xp: int = 10, *args, **kwargs) -> None:
        super().__init__(name="player", maxhealth=maxhealth, strength=strength,
                         intelligence=intelligence, charisma=charisma,
                         dexterity=dexterity, constitution=constitution,
                         level=level, *args, **kwargs)
        self.current_xp = current_xp
        self.max_xp = max_xp
        self.inventory = list()
        self.paths = dict()

    def move(self, y: int, x: int) -> None:
        """
        When the player moves, move the camera of the map.
        """
        super().move(y, x)
        self.map.currenty = y
        self.map.currentx = x
        self.recalculate_paths()

    def level_up(self) -> None:
        """
        Add levels to the player as much as it is possible.
        """
        while self.current_xp > self.max_xp:
            self.level += 1
            self.current_xp -= self.max_xp
            self.max_xp = self.level * 10
            self.health = self.maxhealth
            # TODO Remove it, that's only fun
            self.map.spawn_random_entities(randint(3 * self.level,
                                                   10 * self.level))

    def add_xp(self, xp: int) -> None:
        """
        Add some experience to the player.
        If the required amount is reached, level up.
        """
        self.current_xp += xp
        self.level_up()

    # noinspection PyTypeChecker,PyUnresolvedReferences
    def check_move(self, y: int, x: int, move_if_possible: bool = False) \
            -> bool:
        """
        If the player tries to move but a fighting entity is there,
        the player fights this entity.
        It rewards some XP if it is dead.
        """
        # Don't move if we are dead
        if self.dead:
            return False
        for entity in self.map.entities:
            if entity.y == y and entity.x == x:
                if entity.is_fighting_entity():
                    self.hit(entity)
                    if entity.dead:
                        self.add_xp(randint(3, 7))
                    return True
                elif entity.is_item():
                    entity.hold(self)
        return super().check_move(y, x, move_if_possible)

    def recalculate_paths(self, max_distance: int = 8) -> None:
        """
        Use Dijkstra algorithm to calculate best paths
        for monsters to go to the player.
        """
        queue = [(self.y, self.x)]
        visited = []
        distances = {(self.y, self.x): 0}
        predecessors = {}
        while queue:
            y, x = queue.pop(0)
            visited.append((y, x))
            if distances[(y, x)] >= max_distance:
                continue
            for diff_y, diff_x in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_y, new_x = y + diff_y, x + diff_x
                if not 0 <= new_y < self.map.height or \
                        not 0 <= new_x < self.map.width or \
                        not self.map.tiles[y][x].can_walk() or \
                        (new_y, new_x) in visited or \
                        (new_y, new_x) in queue:
                    continue
                predecessors[(new_y, new_x)] = (y, x)
                distances[(new_y, new_x)] = distances[(y, x)] + 1
                queue.append((new_y, new_x))
        self.paths = predecessors

    def save_state(self) -> dict:
        """
        Saves the state of the entity into a dictionary
        """
        d = super().save_state()
        d["current_xp"] = self.current_xp
        d["max_xp"] = self.max_xp
        return d
