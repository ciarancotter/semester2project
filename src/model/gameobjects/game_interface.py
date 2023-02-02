"""This is the module that a view would use to interact with a game object to get info about the game state.

This module contains 2 classes PlatformerGame and CtxToRender. PlatformerGame is the class that contains all
the information that is required store and update the gamestate(information about the game like charictar
position) from frame to frame. It returns CtxToRender which contains all the information needed to
display this gamestate to the user.

Typical usage example:

game = PlatformerGame()
ctx = game.get_render_ctx()
for block in ctx.blocks:
	print(block.coordinates)
# print the coordinates of all the blocks in the game
"""

class PlatformerGame(object):
	""" The main game class that stores the gamestate."""
	def __init__(self):
		# initialise all the objects
		self._enemies = []
		self._player = " a player object"
		self._blocks = []
		self._entities = []
		self._ctx = CtxToRender()
	def get_render_ctx(self) -> CtxToRender:
		"""Returns the information necicary (or the context/shortend to ctx in this program ) to render
		the game visualy.

		Returns:
			a CtxToRender object containing the necicary rendering information.

		"""
		return self.CtxToRender()



class CtxToRender(object):
	def __init__(self,enemies,player,blocks,entities):
		"""contains all the information needed to 
		display a gamestate to the user.

		meant to be used as a container to be passed to 
		a module using a game engine but attempts to be
		platform independent.

		Args:
			enemies: a list of enemy objects to be displayed
			on the screen
			player: a player object representing main charicter
			blocks: a list of block platforms
			entities: a list of all the perivios entities together 

		"""
		self._enemies = enemies
		self._player = player
		self._blocks = blocks
		self._entities = entities
	
	def get_entities(self):
		return self._entities
	def get_player(self):
		return self._player
	def get_blocks(self):
		return self._blocks
	def get_enemies(self):
		return self._enemies

	enemies = property(get_enemies)
	player = property(get_player)
	blocks = property(get_blocks)
	entities = property(get_entities)
	
