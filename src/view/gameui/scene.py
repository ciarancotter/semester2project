"""A module containing the class to handle the rendering of objects onto a Pygame window.

The Scene class represents the collected elements that should be drawn to
a screen. This is information is obtained from the PlatformerGame object in
the model directory. The Scene may change depending on the state of the game - 
for example, if the game state is the Menu screen, then the Menu UI elements will
be rendered in the Pygame window.

Usage:

    myScene = Scene(myGameManager)
    myScene.initialiseGameScene()
    myScene.drawBackground(GameState.start_menu)
    myScene.updateScene()
"""

import os
import sys
import enum
import pygame

sys.path.append(os.path.abspath("./src"))

from model.gameobjects.entity_unittest import TestPlayer
from model.gameobjects.game_interface import PlatformerGame
from model.gameobjects.public_enums import GameState, Movement
from model.gameobjects.entity_unittest import TestPlayer

from model.aiutilities.aiutilities import generate_background


class Scene:
    """A class representing the elements that should be rendered in a Pygame window.

    The Scene object is created and managed by the PlatformerGame class. Where the PlatformerGame
    class controls game state, the Scene class renders the state to the Pygame window.

    Attributes:
        game_manager: The PlatformerGame object that contains all of the game's current state data.
        
    """

    def __init__(self, game_manager: PlatformerGame):
        """Inits the Scene class.
        """
        pygame.init()
        
        self.game_manager = game_manager
        self.player = None
        self.background = None
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1024, 768))

        menu_background = pygame.image.load("src/view/assets/menuBG.png").convert_alpha()
        transformed_menu_background = pygame.transform.scale(background, (1024, 768))
    
        game_background = pygame.image.load("src/view/assets/menuBG.png").convert_alpha()
        transformed_game_background = pygame.transform.scale(background, (768, 768))

    def drawBackground(gamestate):
        """Draws the background depending on the current state of the game.
        """

        if gamestate == GameState.start_menu:
            self.background = transformed_menu_background

        elif gamestate == GameState.in_session:
            self.background = transformed_game_background

        screen.blit(self.background, (0, 0))

    def initialiseGameScene(self):
        """Run once when the game is created. Generates the AI data.
        """

        pygame.display.set_caption("Boole Raider")
        generate_background("ancient Egypt")
        drawBackground(GameState.in_session)

    def initialiseMenuScene(self):
        
        pygame.display.set_caption("Main Menu")
        logo_base = pygame.image.load("src/view/assets/logo.png")
        logo = pygame.transform.scale(logo_base, (800, 150))
        logo_rect = logo.get_rect()
        logo_rect.center = (512, 150)
        font = pygame.font.Font(None, 85)

    def updateScene(self):
        """Updates the current scene.

        This method checks whether the current scene is the start menu, or 
        the game itself. The result of this check determines what will be rendered
        in the scene
        """
        
        # Fetches the current game state
        current_scene = self.game_manager.get_render_ctx
        # Decides what to draw
        if current_scene.game_state == GameState.in_session:
            drawBackground(GameState.in_session)

        elif current_scene.game_state == GameState.start_menu:
            
            BLACK = (0, 0, 0)
            BLUE = (104, 119, 225)
            
            drawBackground(GameState.start_menu)
            
# Anything above here has been cleaned up, and anything below here is a work in progress.

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


            after_play = TestPlayer()

            running = True

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    # Check if play button is clicked
                    if event.type == pygame.MOUSEBUTTONUP and play_rect.collidepoint(event.pos):
                        after_play.run_after_play_button()
                mouse_pos = pygame.mouse.get_pos()

                if play_rect.collidepoint(mouse_pos):
                    play_button = font.render("PLAY", True, BLUE)
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                else:
                    play_button = font.render("PLAY", True, BLACK)
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)


                # Check if mouse is hovering over buttons and effect
                if play_rect.collidepoint(mouse_pos):
                    play_button = font.render("PLAY", True, BLUE)
                else:
                    play_button = font.render("PLAY", True, BLACK)

                if leaderboard_rect.collidepoint(mouse_pos):
                    leaderboard_button = font.render("LEADERBOARD", True, BLUE)
                else:
                    leaderboard_button = font.render("LEADERBOARD", True, BLACK)

                if help_rect.collidepoint(mouse_pos):
                    help_button = font.render("HELP", True, BLUE)
                else:
                    help_button = font.render("HELP", True, BLACK)

                if about_rect.collidepoint(mouse_pos):
                    about_button = font.render("ABOUT", True, BLUE)
                else:
                    about_button = font.render("ABOUT", True, BLACK)

                # Draw buttons
                screen.blit(play_button, play_rect)
                screen.blit(leaderboard_button, leaderboard_rect)
                screen.blit(help_button, help_rect)
                screen.blit(about_button, about_rect)

                pygame.display.update()

                pygame.quit()
                sys.exit()
            sys.exit()

        else:
            print("Invalid gamestate!")
