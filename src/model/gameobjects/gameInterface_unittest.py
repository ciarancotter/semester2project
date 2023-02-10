import unittest
from game_interface import PlatformerGame, Movement, CtxToRender

class testPlatformerGame(unittest.TestCase):
	def testGetCtx(self):
		testPlatformerGame = PlatformerGame()
		testPlatformerGame.update_model(Movement.left)
		ctx = testPlatformerGame.get_render_ctx()
		self.assertEqual(ctx.player.xPos,382)
