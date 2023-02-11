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

            pygame.init()

            # Set screen size and title
            screen = pygame.display.set_mode((1024, 768))
            pygame.display.set_caption("Main Menu")

            # Define colors
            BLACK = (0, 0, 0)

            # Load background image
            background = pygame.image.load("src/view/assets/menuBG.png")
            background = pygame.transform.scale(background, (1024, 768))

            logo = pygame.image.load("src/view/assets/logo.png")
            logo = pygame.transform.scale(logo, (800, 150))

            # Define font and size
            font = pygame.font.Font(None, 85)

            # Get the rectangle for the image
            logo_rect = logo.get_rect()

            # Set the position of the image on the screen
            logo_rect.center = (512, 150)

            # Draw background
            screen.blit(background, (0, 0))

            # Draw logo
            screen.blit(logo, logo_rect)

            # Define buttons
            play_button = font.render("PLAY", True, BLACK)
            play_rect = play_button.get_rect()
            play_rect.center = (512, 330)

            leaderboard_button = font.render("LEADERBOARD", True, BLACK)
            leaderboard_rect = leaderboard_button.get_rect()
            leaderboard_rect.center = (512, 430)

            help_button = font.render("HELP", True, BLACK)
            help_rect = help_button.get_rect()
            help_rect.center = (512, 530)

            about_button = font.render("ABOUT", True, BLACK)
            about_rect = about_button.get_rect()
            about_rect.center = (512, 630)

                #pygame.display.update()

            pygame.quit()
            sys.exit()

            pass
        else:
            print("Invalid gamestate!")

         # method for pygame loop'''

    