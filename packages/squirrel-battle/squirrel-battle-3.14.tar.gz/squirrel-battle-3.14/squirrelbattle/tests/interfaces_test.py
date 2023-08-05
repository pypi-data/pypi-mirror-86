import unittest

from squirrelbattle.display.texturepack import TexturePack
from squirrelbattle.interfaces import Map, Tile
from squirrelbattle.resources import ResourceManager


class TestInterfaces(unittest.TestCase):
    def test_map(self) -> None:
        """
        Create a map and check that it is well parsed.
        """
        m = Map.load_from_string("0 0\n.#\n#.\n")
        self.assertEqual(m.width, 2)
        self.assertEqual(m.height, 2)
        self.assertEqual(m.draw_string(TexturePack.ASCII_PACK), ".#\n#.")

    def test_load_map(self) -> None:
        """
        Try to load a map from a file.
        """
        m = Map.load(ResourceManager.get_asset_path("example_map.txt"))
        self.assertEqual(m.width, 52)
        self.assertEqual(m.height, 17)

    def test_tiles(self) -> None:
        """
        Test some things about tiles.
        """
        self.assertFalse(Tile.FLOOR.is_wall())
        self.assertTrue(Tile.WALL.is_wall())
        self.assertFalse(Tile.EMPTY.is_wall())
        self.assertTrue(Tile.FLOOR.can_walk())
        self.assertFalse(Tile.WALL.can_walk())
        self.assertFalse(Tile.EMPTY.can_walk())
        self.assertRaises(ValueError, Tile.from_ascii_char, 'unknown')
