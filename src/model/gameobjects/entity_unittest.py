import unittest
from entity import Player
from entity import Block
from entity import Entity
from game_interface import Movement

class TestPlayer(unittest.TestCase):
	"""the  tests for the player object """
	def test_collide(self):
		""" check that the player. collide is working """
		play = Player(50,50,1000,1000)
		blocks = [Block(Entity(500,551,32,32,True))]
		print(type(blocks))
		collide_test = play.collideTop(blocks)
		self.assertTrue(collide_test,"not correct")
	def test_update(self):
		testPlayer = Player(50,50,1000,1000)
		testPlayer.move(Movement.no_movement,[])
		self.assertEqual(testPlayer.yPos,502,"gravity not working")
