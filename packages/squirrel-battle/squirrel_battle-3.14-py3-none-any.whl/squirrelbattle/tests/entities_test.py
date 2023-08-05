import unittest

from squirrelbattle.entities.items import Bomb, Heart, Item
from squirrelbattle.entities.monsters import Beaver, Hedgehog, Rabbit, TeddyBear
from squirrelbattle.entities.player import Player
from squirrelbattle.interfaces import Entity, Map
from squirrelbattle.resources import ResourceManager


class TestEntities(unittest.TestCase):
    def setUp(self) -> None:
        """
        Load example map that can be used in tests.
        """
        self.map = Map.load(ResourceManager.get_asset_path("example_map.txt"))
        self.player = Player()
        self.map.add_entity(self.player)
        self.player.move(self.map.start_y, self.map.start_x)

    def test_basic_entities(self) -> None:
        """
        Test some random stuff with basic entities.
        """
        entity = Entity()
        entity.move(42, 64)
        self.assertEqual(entity.y, 42)
        self.assertEqual(entity.x, 64)
        self.assertIsNone(entity.act(self.map))

        other_entity = Entity()
        other_entity.move(45, 68)
        self.assertEqual(entity.distance_squared(other_entity), 25)
        self.assertEqual(entity.distance(other_entity), 5)

    def test_fighting_entities(self) -> None:
        """
        Test some random stuff with fighting entities.
        """
        entity = Beaver()
        self.map.add_entity(entity)
        self.assertEqual(entity.maxhealth, 20)
        self.assertEqual(entity.maxhealth, entity.health)
        self.assertEqual(entity.strength, 2)
        for _ in range(9):
            self.assertIsNone(entity.hit(entity))
            self.assertFalse(entity.dead)
        self.assertIsNone(entity.hit(entity))
        self.assertTrue(entity.dead)

        entity = Rabbit()
        self.map.add_entity(entity)
        entity.move(15, 44)
        # Move randomly
        self.map.tick()
        self.assertFalse(entity.y == 15 and entity.x == 44)

        # Move to the player
        entity.move(3, 6)
        self.map.tick()
        self.assertTrue(entity.y == 2 and entity.x == 6)

        # Rabbit should fight
        old_health = self.player.health
        self.map.tick()
        self.assertTrue(entity.y == 2 and entity.x == 6)
        self.assertEqual(old_health - entity.strength, self.player.health)

        # Fight the rabbit
        old_health = entity.health
        self.player.move_down()
        self.assertEqual(entity.health, old_health - self.player.strength)
        self.assertFalse(entity.dead)
        old_health = entity.health
        self.player.move_down()
        self.assertEqual(entity.health, old_health - self.player.strength)
        self.assertFalse(entity.dead)
        old_health = entity.health
        self.player.move_down()
        self.assertEqual(entity.health, old_health - self.player.strength)
        self.assertTrue(entity.dead)
        self.assertGreaterEqual(self.player.current_xp, 3)

    def test_items(self) -> None:
        """
        Test some random stuff with items.
        """
        item = Item()
        self.map.add_entity(item)
        self.assertFalse(item.held)
        item.hold(self.player)
        self.assertTrue(item.held)
        item.drop(2, 6)
        self.assertEqual(item.y, 2)
        self.assertEqual(item.x, 6)

        # Pick up item
        self.player.move_down()
        self.assertTrue(item.held)
        self.assertEqual(item.held_by, self.player)
        self.assertIn(item, self.player.inventory)
        self.assertNotIn(item, self.map.entities)

    def test_bombs(self) -> None:
        """
        Test some random stuff with bombs.
        """
        item = Bomb()
        hedgehog = Hedgehog()
        teddy_bear = TeddyBear()
        self.map.add_entity(item)
        self.map.add_entity(hedgehog)
        self.map.add_entity(teddy_bear)
        hedgehog.health = 2
        teddy_bear.health = 2
        hedgehog.move(41, 42)
        teddy_bear.move(42, 41)
        item.act(self.map)
        self.assertFalse(hedgehog.dead)
        self.assertFalse(teddy_bear.dead)
        item.drop(42, 42)
        self.assertEqual(item.y, 42)
        self.assertEqual(item.x, 42)
        item.act(self.map)
        self.assertTrue(hedgehog.dead)
        self.assertTrue(teddy_bear.dead)
        bomb_state = item.save_state()
        self.assertEqual(bomb_state["damage"], item.damage)

    def test_hearts(self) -> None:
        """
        Test some random stuff with hearts.
        """
        item = Heart()
        self.map.add_entity(item)
        item.move(2, 6)
        self.player.health -= 2 * item.healing
        self.player.move_down()
        self.assertNotIn(item, self.map.entities)
        self.assertEqual(self.player.health,
                         self.player.maxhealth - item.healing)
        heart_state = item.save_state()
        self.assertEqual(heart_state["healing"], item.healing)

    def test_players(self) -> None:
        """
        Test some random stuff with players.
        """
        player = Player()
        self.map.add_entity(player)
        player.move(1, 6)
        self.assertEqual(player.strength, 5)
        self.assertEqual(player.health, player.maxhealth)
        self.assertEqual(player.maxhealth, 20)

        # Test movements and ensure that collisions are working
        self.assertFalse(player.move_up())
        self.assertTrue(player.move_left())
        self.assertFalse(player.move_left())
        for i in range(8):
            self.assertTrue(player.move_down())
        self.assertFalse(player.move_down())
        self.assertTrue(player.move_right())
        self.assertTrue(player.move_right())
        self.assertTrue(player.move_right())
        self.assertFalse(player.move_right())
        self.assertTrue(player.move_down())
        self.assertTrue(player.move_down())

        player.add_xp(70)
        self.assertEqual(player.current_xp, 10)
        self.assertEqual(player.max_xp, 40)
        self.assertEqual(player.level, 4)

        player_state = player.save_state()
        self.assertEqual(player_state["current_xp"], 10)
