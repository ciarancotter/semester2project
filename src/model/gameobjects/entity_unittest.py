import unittest
from entity import Player
from entity import Block
from entity import Entity

class TestPlayer(unittest.TestCase):
	def test_collide(self):
		play = Player(50,50,1000,1000)
		blocks = [Block(Entity(500,551,32,32,True))]
		print(type(blocks))
		collide_test = play.collideTop(blocks)
		self.assertTrue(collide_test,"not correct")