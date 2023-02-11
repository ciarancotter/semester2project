import enum
import sys
import os
sys.path.append(os.path.abspath("./src"))
from model.gameobjects.game_interface import PlatformerGame
from model.gameobjects.public_enums import GameState, Movement
from button import Button
import pygame


class Scene:

    def __init__(self, game_manager: PlatformerGame):
        self.game_manager = game_manager
        self.player = None
        self.background = None
        self.clock = pygame.time.Clock()

    def updateScene(self):
        current_scene = self.game_manager.get_render_ctx
        if current_scene.game_state == GameState.in_session:
            # Draw game!
            pass

        elif current_scene.game_state == GameState.start_menu:
            # Draw menu!
            pass
        else:
            print("Invalid gamestate!")

         # method for pygame loop'''

    