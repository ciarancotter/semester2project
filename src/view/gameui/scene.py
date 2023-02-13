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

from .uielements import Button

from model.gameobjects.game_interface import PlatformerGame
from model.gameobjects.public_enums import GameState, Movement

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
        self.menu_buttons = []

        menu_background = pygame.image.load("src/view/assets/menuBG.png").convert_alpha()
        self.transformed_menu_background = pygame.transform.scale(menu_background, (1024, 768))

        game_background = pygame.image.load("src/view/assets/menuBG.png").convert_alpha()
        self.transformed_game_background = pygame.transform.scale(game_background, (768, 768))

        BLACK = (0, 0, 0)
        BLUE = (104, 119, 225)

        #following variables is to be used for drawing player 


        self.sprite_sheet = pygame.image.load("src/view/assets/playerSprite.png").convert_alpha()
        # set the starting sprite for the character
        self.current_sprite_index = 0
        self.character_sprites = [pygame.Surface((game_manager.get_render_ctx.get_player.get_width(),game_manager.get_render_ctx.get_player.get_height()), pygame.SRCALPHA) for i in range(columns * rows)]
        self.columns = 3
        self.rows = 2
        #shortcut for player data that we're getting from render_ctx
        self.player_data = self.game_manager.get_render_ctx.get_player
        # set the delay between each frame
        self.frame_delay = 5
        self.frame_count = 0
        self.direction = "right"


    def drawBackground(self, game_state):
        """Draws the background depending on the current state of the game.
        """

        if game_state == GameState.start_menu:
            self.background = self.transformed_menu_background

        elif game_state == GameState.in_session:
            self.background = self.transformed_game_background

        self.screen.blit(self.background, (0, 0))

    def drawLogo(self):
        """Draws the logo
        """
        logo_base = pygame.image.load("src/view/assets/logo.png")
        logo = pygame.transform.scale(logo_base, (800, 150))
        logo_rect = logo.get_rect()
        logo_rect.center = (512, 150)
        self.screen.blit(logo, logo_rect)

    def initialiseGameScene(self):
        """Run once when the game is created. Generates the AI data.
        """

        pygame.display.set_caption("Boole Raider")
        generate_background("ancient Egypt")
        self.drawBackground(GameState.in_session)

    def initialiseMenuScene(self):
        """Initialises elements for the menu scene.
        """
        pygame.display.set_caption("Main Menu")

        play_button = Button("PLAY", (512, 330))
        leaderboard_button = Button("LEADERBOARD", (512, 430))
        help_button = Button("HELP", (512, 530))
        about_button = Button("ABOUT", (512, 630))

        self.menu_buttons.append(play_button)
        self.menu_buttons.append(leaderboard_button)
        self.menu_buttons.append(help_button)
        self.menu_buttons.append(about_button)

        # Draw buttons
        for button in self.menu_buttons:
            self.screen.blit(button.renderer, button.rect)

        # Draw logo
        self.drawLogo()

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
            self.drawBackground(GameState.in_session)
            # Draw the players and enemies! @Shaza
            player_data = self.game_manager.get_render_ctx
            for i in range(self.rows):
                for j in range(self.columns):
                    self.drawBackground(GameState.in_session)
                    self.character_sprites[i * self.columns + j].blit(self.sprite_sheet, (0, 0), (j * self.player_data.get_width(), i * self.player_data.get_height(), self.player_data.get_width(), self.player_data.get_height()))

            # move the character to the right if the right key is pressed
            if self.player_data.facing == Movement.right:
                #x += 1
                self.player_data.move(self.player_data.facing,[])
                self.direction = "right"
                self.frame_count += 1
                if self.frame_count == self.frame_delay:
                    self.current_sprite_index = (self.current_sprite_index + 1) % self.columns
                    self.frame_count = 0
            
            # move the character to the left if the left key is pressed

            if self.player_data.facing == Movement.left:
                #x += 1
                self.player_data.move(self.player_data.facing,[])
                self.direction = "left"
                self.frame_count += 1
                if self.frame_count == self.frame_delay:
                    self.current_sprite_index = self.columns + (self.current_sprite_index + 2) % self.columns
                    self.frame_count = 0
                    
            # move the character to the up if the space key is pressed

            if self.player_data.facing == Movement.jump:
                self.player_data.move(self.player_data.facing,[])
                self.direction = "jump"
                self.frame_count += 1
                if self.frame_count == self.frame_delay:
                    self.current_sprite_index = self.current_sprite_index 
                    self.frame_count = 0
            
            #TODO punch picture and code 

            # update the current sprite based on the direction of the character
            if self.direction == "right":
                if self.current_sprite_index < self.columns:
                    self.drawBackground(GameState.in_session)
                    self.screen.blit(self.character_sprites[self.current_sprite_index], (self.player_data.xPos, self.player_data.yPos))
            else:
                if self.current_sprite_index >= self.columns:
                    self.drawBackground(GameState.in_session)
                    self.screen.blit(self.character_sprites[self.current_sprite_index], (self.player_data.xPos, self.player_data.yPos))

                

        elif current_scene.game_state == GameState.start_menu:
            self.drawBackground(GameState.start_menu)
            self.drawLogo()

    def checking_hover(self, mouse_pos:tuple):
        """check for hovering over the buttons in menue
            This method checks whether the mouse over any buttons start menu which is an array,
             Attributes:
                 menu_buttons: an array of menu buttons
            """
        for button in self.menu_buttons:
            if button.rect.collidepoint(mouse_pos):
                button.setBlue()
