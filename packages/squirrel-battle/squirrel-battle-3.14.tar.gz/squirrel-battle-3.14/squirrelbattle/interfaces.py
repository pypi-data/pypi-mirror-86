#!/usr/bin/env python
from enum import Enum, auto
from math import sqrt
from random import choice, randint
from typing import List, Optional

from squirrelbattle.display.texturepack import TexturePack


class Map:
    """
    Object that represents a Map with its width, height
    and tiles, that have their custom properties.
    """
    width: int
    height: int
    start_y: int
    start_x: int
    tiles: List[List["Tile"]]
    entities: List["Entity"]
    # coordinates of the point that should be
    # on the topleft corner of the screen
    currentx: int
    currenty: int

    def __init__(self, width: int, height: int, tiles: list,
                 start_y: int, start_x: int):
        self.width = width
        self.height = height
        self.start_y = start_y
        self.start_x = start_x
        self.tiles = tiles
        self.entities = []

    def add_entity(self, entity: "Entity") -> None:
        """
        Register a new entity in the map.
        """
        self.entities.append(entity)
        entity.map = self

    def remove_entity(self, entity: "Entity") -> None:
        """
        Unregister an entity from the map.
        """
        self.entities.remove(entity)

    def find_entities(self, entity_class: type) -> list:
        return [entity for entity in self.entities
                if isinstance(entity, entity_class)]

    def is_free(self, y: int, x: int) -> bool:
        """
        Indicates that the case at the coordinates (y, x) is empty.
        """
        return 0 <= y < self.height and 0 <= x < self.width and \
            self.tiles[y][x].can_walk() and \
            not any(entity.x == x and entity.y == y for entity in self.entities)

    @staticmethod
    def load(filename: str) -> "Map":
        """
        Read a file that contains the content of a map, and build a Map object.
        """
        with open(filename, "r") as f:
            file = f.read()
        return Map.load_from_string(file)

    @staticmethod
    def load_from_string(content: str) -> "Map":
        """
        Load a map represented by its characters and build a Map object.
        """
        lines = content.split("\n")
        first_line = lines[0]
        start_y, start_x = map(int, first_line.split(" "))
        lines = [line for line in lines[1:] if line]
        height = len(lines)
        width = len(lines[0])
        tiles = [[Tile.from_ascii_char(c)
                  for x, c in enumerate(line)] for y, line in enumerate(lines)]

        return Map(width, height, tiles, start_y, start_x)

    @staticmethod
    def load_dungeon_from_string(content: str) -> List[List["Tile"]]:
        """
        Transforms a string into the list of corresponding tiles
        """
        lines = content.split("\n")
        tiles = [[Tile.from_ascii_char(c)
                  for x, c in enumerate(line)] for y, line in enumerate(lines)]
        return tiles

    def draw_string(self, pack: TexturePack) -> str:
        """
        Draw the current map as a string object that can be rendered
        in the window.
        """
        return "\n".join("".join(tile.char(pack) for tile in line)
                         for line in self.tiles)

    def spawn_random_entities(self, count: int) -> None:
        """
        Put randomly {count} hedgehogs on the map, where it is available.
        """
        for _ in range(count):
            y, x = 0, 0
            while True:
                y, x = randint(0, self.height - 1), randint(0, self.width - 1)
                tile = self.tiles[y][x]
                if tile.can_walk():
                    break
            entity = choice(Entity.get_all_entity_classes())()
            entity.move(y, x)
            self.add_entity(entity)

    def tick(self) -> None:
        """
        Trigger all entity events.
        """
        for entity in self.entities:
            entity.act(self)

    def save_state(self) -> dict:
        """
        Saves the map's attributes to a dictionary
        """
        d = dict()
        d["width"] = self.width
        d["height"] = self.height
        d["start_y"] = self.start_y
        d["start_x"] = self.start_x
        d["currentx"] = self.currentx
        d["currenty"] = self.currenty
        d["entities"] = []
        for enti in self.entities:
            d["entities"].append(enti.save_state())
        d["map"] = self.draw_string(TexturePack.ASCII_PACK)
        return d

    def load_state(self, d: dict) -> None:
        """
        Loads the map's attributes from a dictionary
        """
        self.width = d["width"]
        self.height = d["height"]
        self.start_y = d["start_y"]
        self.start_x = d["start_x"]
        self.currentx = d["currentx"]
        self.currenty = d["currenty"]
        self.tiles = self.load_dungeon_from_string(d["map"])
        self.entities = []
        dictclasses = Entity.get_all_entity_classes_in_a_dict()
        for entisave in d["entities"]:
            self.add_entity(dictclasses[entisave["type"]](**entisave))


class Tile(Enum):
    """
    The internal representation of the tiles of the map
    """
    EMPTY = auto()
    WALL = auto()
    FLOOR = auto()

    @staticmethod
    def from_ascii_char(ch: str) -> "Tile":
        """
        Maps an ascii character to its equivalent in the texture pack
        """
        for tile in Tile:
            if tile.char(TexturePack.ASCII_PACK) == ch:
                return tile
        raise ValueError(ch)

    def char(self, pack: TexturePack) -> str:
        """
        Translates a Tile to the corresponding character according
        to the texture pack
        """
        return getattr(pack, self.name)

    def is_wall(self) -> bool:
        """
        Is this Tile a wall?
        """
        return self == Tile.WALL

    def can_walk(self) -> bool:
        """
        Check if an entity (player or not) can move in this tile.
        """
        return not self.is_wall() and self != Tile.EMPTY


class Entity:
    """
    An Entity object represents any entity present on the map
    """
    y: int
    x: int
    name: str
    map: Map

    # noinspection PyShadowingBuiltins
    def __init__(self, y: int = 0, x: int = 0, name: Optional[str] = None,
                 map: Optional[Map] = None, *ignored, **ignored2):
        self.y = y
        self.x = x
        self.name = name
        self.map = map

    def check_move(self, y: int, x: int, move_if_possible: bool = False)\
            -> bool:
        """
        Checks if moving to (y,x) is authorized
        """
        free = self.map.is_free(y, x)
        if free and move_if_possible:
            self.move(y, x)
        return free

    def move(self, y: int, x: int) -> bool:
        """
        Moves an entity to (y,x) coordinates
        """
        self.y = y
        self.x = x
        return True

    def move_up(self, force: bool = False) -> bool:
        """
        Moves the entity up one tile, if possible
        """
        return self.move(self.y - 1, self.x) if force else \
            self.check_move(self.y - 1, self.x, True)

    def move_down(self, force: bool = False) -> bool:
        """
        Moves the entity down one tile, if possible
        """
        return self.move(self.y + 1, self.x) if force else \
            self.check_move(self.y + 1, self.x, True)

    def move_left(self, force: bool = False) -> bool:
        """
        Moves the entity left one tile, if possible
        """
        return self.move(self.y, self.x - 1) if force else \
            self.check_move(self.y, self.x - 1, True)

    def move_right(self, force: bool = False) -> bool:
        """
        Moves the entity right one tile, if possible
        """
        return self.move(self.y, self.x + 1) if force else \
            self.check_move(self.y, self.x + 1, True)

    def act(self, m: Map) -> None:
        """
        Define the action of the entity that is ran each tick.
        By default, does nothing.
        """
        pass

    def distance_squared(self, other: "Entity") -> int:
        """
        Get the square of the distance to another entity.
        Useful to check distances since square root takes time.
        """
        return (self.y - other.y) ** 2 + (self.x - other.x) ** 2

    def distance(self, other: "Entity") -> float:
        """
        Get the cartesian distance to another entity.
        """
        return sqrt(self.distance_squared(other))

    def is_fighting_entity(self) -> bool:
        """
        Is this entity a fighting entity?
        """
        return isinstance(self, FightingEntity)

    def is_item(self) -> bool:
        """
        Is this entity an item?
        """
        from squirrelbattle.entities.items import Item
        return isinstance(self, Item)

    @staticmethod
    def get_all_entity_classes():
        """
        Returns all entities subclasses
        """
        from squirrelbattle.entities.items import Heart, Bomb
        from squirrelbattle.entities.monsters import Beaver, Hedgehog, \
            Rabbit, TeddyBear
        return [Beaver, Bomb, Heart, Hedgehog, Rabbit, TeddyBear]

    @staticmethod
    def get_all_entity_classes_in_a_dict() -> dict:
        """
        Returns all entities subclasses in a dictionary
        """
        from squirrelbattle.entities.player import Player
        from squirrelbattle.entities.monsters import Beaver, Hedgehog, Rabbit, \
            TeddyBear
        from squirrelbattle.entities.items import Bomb, Heart
        return {
            "Beaver": Beaver,
            "Bomb": Bomb,
            "Heart": Heart,
            "Hedgehog": Hedgehog,
            "Rabbit": Rabbit,
            "TeddyBear": TeddyBear,
            "Player": Player,
        }

    def save_state(self) -> dict:
        """
        Saves the coordinates of the entity
        """
        d = dict()
        d["x"] = self.x
        d["y"] = self.y
        d["type"] = self.__class__.__name__
        return d


class FightingEntity(Entity):
    """
    A FightingEntity is an entity that can fight, and thus has a health,
    level and stats
    """
    maxhealth: int
    health: int
    strength: int
    intelligence: int
    charisma: int
    dexterity: int
    constitution: int
    level: int

    def __init__(self, maxhealth: int = 0, health: Optional[int] = None,
                 strength: int = 0, intelligence: int = 0, charisma: int = 0,
                 dexterity: int = 0, constitution: int = 0, level: int = 0,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.maxhealth = maxhealth
        self.health = maxhealth if health is None else health
        self.strength = strength
        self.intelligence = intelligence
        self.charisma = charisma
        self.dexterity = dexterity
        self.constitution = constitution
        self.level = level

    @property
    def dead(self) -> bool:
        return self.health <= 0

    def hit(self, opponent: "FightingEntity") -> None:
        """
        Deals damage to the opponent, based on the stats
        """
        opponent.take_damage(self, self.strength)

    def take_damage(self, attacker: "Entity", amount: int) -> None:
        """
        Take damage from the attacker, based on the stats
        """
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self) -> None:
        """
        If a fighting entity has no more health, it dies and is removed
        """
        self.map.remove_entity(self)

    def keys(self) -> list:
        """
        Returns a fighting entities specific attributes
        """
        return ["maxhealth", "health", "level", "strength",
                "intelligence", "charisma", "dexterity", "constitution"]

    def save_state(self) -> dict:
        """
        Saves the state of the entity into a dictionary
        """
        d = super().save_state()
        for name in self.keys():
            d[name] = getattr(self, name)
        return d
