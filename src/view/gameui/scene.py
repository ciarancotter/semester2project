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

from view.gameui.healthbar import HealthBar
from view.gameui.uielements import Button, TextBox, Panel
from model.gameobjects.public_enums import Movement

from model.gameobjects.game_interface import PlatformerGame
from model.gameobjects.public_enums import GameState

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
        self.screen = pygame.display.set_mode((1280, 784))
        self.menu_buttons = []
        self.loadedGame = False

        self.textbox = None
        self.healthbar = None
        self.gameUIPanel = None
        self.mainGamePanel = None

        menu_background = pygame.image.load("src/view/assets/menuBG.png").convert_alpha()
        self.transformed_menu_background = pygame.transform.scale(menu_background, (1280, 784))

        self.transformed_game_background = None
        BLACK = (0, 0, 0)
        BLUE = (104, 119, 225)

        # following variables is to be used for drawing player

        self.sprite_sheet = pygame.image.load("src/view/assets/playerSprite.png").convert_alpha()
        # set the starting sprite for the character
        self.current_sprite_index = 0
        self.columns = 3
        self.rows = 3
        self.context = game_manager.get_render_ctx()
        size = (self.context.player.width, self.context.player.height)
        self.character_sprites = [pygame.Surface(size, pygame.SRCALPHA) for i in range(self.columns * self.rows)]
        # shortcut for player data that we're getting from render_ctx
        self.player_data = self.context.player
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
        logo_rect.center = (640, 150)
        self.screen.blit(logo, logo_rect)
    
    def initialiseGameUIElements(self):
        
        self.mainGamePanel = Panel(self.screen, 784, 512, 0, 0, "black")
        self.mainGamePanel.draw()

        self.gameUIPanel = Panel(self.screen, 496, 784, 784, 0, "orange")
        self.gameUIPanel.draw()

        self.textbox = TextBox(self.screen, 40, 25, "monospace", 16, self.gameUIPanel)
        self.textbox.draw("Monke")

        self.healthbar = HealthBar(self.screen, self.mainGamePanel, 100)
        self.healthbar.drawMaxHealth()
        self.healthbar.drawCurrentHealth()
        print("Should have drawn the health bar")

    def updateGameUIElements(self):
        self.healthbar.drawMaxHealth()
        self.healthbar.drawCurrentHealth()

    def initialiseGameScene(self):
        """Run once when the game is created. Generates the AI data.
        """
        pygame.display.set_caption("Boole Raider")
        generate_background("ancient Egypt")
        self.screen.fill("gold")
        game_background = pygame.image.load("src/view/assets/gamebg.png").convert_alpha()
        self.transformed_game_background = pygame.transform.scale(game_background, (784, 784))
        self.game_manager.set_game_state(GameState.in_session)
        self.drawBackground(GameState.in_session)


    def initialiseMenuScene(self):
        """Initialises elements for the menu scene.
        """
        pygame.display.set_caption("Main Menu")

        play_button = Button("PLAY", (640, 330))
        leaderboard_button = Button("LEADERBOARD", (640, 430))
        help_button = Button("HELP", (640, 530))
        about_button = Button("ABOUT", (640, 630))

        self.menu_buttons.append(play_button)
        self.menu_buttons.append(leaderboard_button)
        self.menu_buttons.append(help_button)
        self.menu_buttons.append(about_button)

    def drawButtons(self):
        # Draw buttons
        for button in self.menu_buttons:
            self.screen.blit(button.renderer, button.rect)

    def updateScene(self):
        """Updates the current scene.

        This method checks whether the current scene is the start menu, or 
        the game itself. The result of this check determines what will be rendered
        in the scene
        """

        # Fetches the current game state
        current_scene = self.game_manager.get_render_ctx()
        # Decides what to draw
        if current_scene.game_state == GameState.in_session:
            self.drawBackground(GameState.in_session)
            self.updateGameUIElements()

            self.player_data = self.game_manager.get_render_ctx().player
            for i in range(self.rows):
                for j in range(self.columns):
                    self.drawBackground(GameState.in_session)
                    self.updateGameUIElements()
                    self.character_sprites[i * self.columns + j].blit(self.sprite_sheet, (0, 0), (
                    j * self.player_data.width, i * self.player_data.height, self.player_data.width,
                    self.player_data.height))
        

            # move the character to the right if the right key is pressed
            if self.player_data.facing == Movement.right:
                # x += 1
                self.direction = "right"
                self.frame_count += 1
                if self.frame_count == self.frame_delay:
                    self.current_sprite_index = (self.current_sprite_index + 1) % self.columns
                    self.frame_count = 0

            # move the character to the left if the left key is pressed

            if self.player_data.facing == Movement.left:
                # x += 1
                self.direction = "left"
                self.frame_count += 1
                if self.frame_count == self.frame_delay:
                    self.current_sprite_index = self.columns + (self.current_sprite_index + 2) % self.columns
                    self.frame_count = 0

            # move the character to the up if the space key is pressed

            if self.player_data.facing == Movement.jump:
                self.direction = "jump"
                self.frame_count += 1
                if self.frame_count == self.frame_delay:
                    self.current_sprite_index = self.current_sprite_index
                    self.frame_count = 0

            if self.player_data.facing == Movement.no_movement:
                self.direction = "no movement"
                self.current_sprite_index = self.current_sprite_index
            
            # right punch picture and code
            if  self.player_data.facing == Movement.right_punch:
                prev_index = self.current_sprite_index
                self.direction = "right punch"
                self.frame_count += 1
                if self.frame_count == self.frame_delay:
                    self.current_sprite_index = 6
                    self.frame_count = 0

                    
            # left punch picture and code
            if  self.player_data.facing == Movement.left_punch:
                self.direction = "right punch"
                self.frame_count += 1
                if self.frame_count == self.frame_delay:
                    self.current_sprite_index = 7
                    self.frame_count = 0
                
            # update the current sprite based on the direction of the character
            if self.direction == "right":
                if self.current_sprite_index < self.columns:
                    self.drawBackground(GameState.in_session)
                    self.updateGameUIElements()
                    self.screen.blit(self.character_sprites[self.current_sprite_index],
                                     (self.player_data.xPos, self.player_data.yPos))
            elif self.direction == "left":
                if self.current_sprite_index >= self.columns:
                    self.drawBackground(GameState.in_session)
                    self.updateGameUIElements()
                    self.screen.blit(self.character_sprites[self.current_sprite_index],
                                     (self.player_data.xPos, self.player_data.yPos))
            elif self.direction == "no movement":
                if self.current_sprite_index >= self.columns:
                    self.drawBackground(GameState.in_session)
                    self.updateGameUIElements()
                    self.screen.blit(self.character_sprites[self.current_sprite_index],
                                     (self.player_data.xPos, self.player_data.yPos))
                if self.current_sprite_index < self.columns:
                    self.drawBackground(GameState.in_session)
                    self.updateGameUIElements()
                    self.screen.blit(self.character_sprites[self.current_sprite_index],
                                     (self.player_data.xPos, self.player_data.yPos))
            elif self.direction == "right punch":
                self.drawBackground(GameState.in_session)
                self.updateGameUIElements()
                self.screen.blit(self.character_sprites[self.current_sprite_index],
                                 (self.player_data.xPos, self.player_data.yPos))
                self.current_sprite_index = 0
                #self.drawBackground(GameState.in_session)
                #self.updateGameUIElements()
                self.screen.blit(self.character_sprites[self.current_sprite_index],
                                 (self.player_data.xPos, self.player_data.yPos))
            elif self.direction == "left punch":
                self.drawBackground(GameState.in_session)
                self.updateGameUIElements()
                self.screen.blit(self.character_sprites[self.current_sprite_index],
                                 (self.player_data.xPos, self.player_data.yPos))
                self.current_sprite_index = 3
                #self.drawBackground(GameState.in_session)
                #self.updateGameUIElements()
                self.screen.blit(self.character_sprites[self.current_sprite_index],
                                 (self.player_data.xPos, self.player_data.yPos))
                


        elif current_scene.game_state == GameState.start_menu:
            self.drawBackground(current_scene.game_state)
            self.drawLogo()
            self.drawButtons()

    def checking_hover(self, mouse_pos: tuple):
        """check for hovering over the buttons in menue
            This method checks whether the mouse over any buttons start menu which is an array,
             Attributes:
                 menu_buttons: an array of menu buttons
            """
        for button in self.menu_buttons:
            if button.rect.collidepoint(mouse_pos):
                button.setBlue()
            else:
                button.setBlack()

    def check_play_pressed(self, event):
        if self.menu_buttons[0].rect.collidepoint(event.pos):
            if not self.loadedGame:
                self.initialiseGameScene()
                self.initialiseGameUIElements()

