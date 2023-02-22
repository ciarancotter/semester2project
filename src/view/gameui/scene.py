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
import pygame

sys.path.append(os.path.abspath("./src"))

from view.gameui.healthbar import HealthBar, LevelIndicator
from view.gameui.uielements import Button, TextBox, Panel
from model.gameobjects.public_enums import Movement

from model.gameobjects.game_interface import PlatformerGame
from model.gameobjects.public_enums import GameState
from model.gameobjects.entity import Block

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
        
        self.door = None
        self.textbox = None
        self.healthbar = None
        self.levelindicator = None
        self.gameUIPanel = None
        self.mainGamePanel = None
        self.blockImage = None

        menu_background = pygame.image.load("src/view/assets/menuBG.png").convert_alpha()
        self.transformed_menu_background = pygame.transform.scale(menu_background, (1280, 784))

        door_image = pygame.image.load("src/view/assets/door.png").convert_alpha() 
        self.doorImage = pygame.transform.scale(door_image, (56, 56))

        self.transformed_game_background = None
        self.sprite_sheet = pygame.image.load("src/view/assets/playerSprite.png").convert_alpha()
        self.sprite_sheet_mummy = pygame.image.load("src/view/assets/mummy_spritesheet.png").convert_alpha()

        # set the starting sprite for the character
        self.current_sprite_index = 0
        self.columns = 3
        self.rows = 3
        self.enemy_columns= 3
        self.enemy_rows = 2        
        self.context = game_manager.get_render_ctx()
        size = (self.context.player.width, self.context.player.height)
        self.character_sprites = [pygame.Surface(size, pygame.SRCALPHA) for i in range(self.columns * self.rows)]

        # shortcut for player data that we're getting from render_ctx
        self.player_data = self.context.player

        # set the delay between each frame
        self.frame_delay = 5
        self.frame_count = 0
        self.direction = "right"
        self.blockImage = pygame.image.load("src/view/assets/block2.png").convert_alpha()

        # Sounds
        #self.punch_sound = pygame.mixer.Sound("src/view/assets/punch.mp3")

    def drawBackground(self, game_state):
        """Draws the background depending on the current state of the game.
        """

        if game_state == GameState.start_menu:
            self.background = self.transformed_menu_background

        elif game_state == GameState.in_session:
            self.background = self.transformed_game_background

        self.screen.blit(self.background, (0, 0))
   

    def drawBradley(self):
        bradley_base = pygame.image.load("src/view/assets/bradley.png")
        bradley = pygame.transform.scale(bradley_base, (244, 244))
        bradley_rekt = bradley.get_rect()
        bradley_rekt.center = (640, 200)
        self.screen.blit(bradley, bradley_rekt)


    def drawLogo(self):
        """Draws the logo.
        """
        logo_base = pygame.image.load("src/view/assets/logo.png")
        logo = pygame.transform.scale(logo_base, (800, 150))
        logo_rect = logo.get_rect()
        logo_rect.center = (640, 150)
        self.screen.blit(logo, logo_rect)
    

    def loading_screen(self):
        """Draws a loading screen.
        """
        self.screen.fill("black")
        self.drawBradley()
        loading_text = pygame.font.SysFont("monospace", 30).render('Loading...', True, "white")
        loading_text_rect = loading_text.get_rect()
        loading_text_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        self.screen.blit(loading_text, loading_text_rect)
        pygame.display.update()


    def initialiseGameUIElements(self):
        """Initialises and draws the main UI elements to the game.
        """

        self.mainGamePanel = Panel(self.screen, 784, 512, 0, 0, "black")
        self.mainGamePanel.draw()

        self.gameUIPanel = Panel(self.screen, 496, 784, 784, 0, "orange")
        self.gameUIPanel.draw()

        self.textbox = TextBox(self.screen, 40, 25, "monospace", 16, self.gameUIPanel)
        self.textbox.draw("Monke")

        self.healthbar = HealthBar(self.screen, self.mainGamePanel, 100)
        self.healthbar.drawMaxHealth()
        self.healthbar.drawCurrentHealth()
        
        self.levelindicator = LevelIndicator(self.screen, self.gameUIPanel)


    def updateGameUIElements(self, current_scene):
        self.healthbar.drawMaxHealth()
        self.healthbar.drawCurrentHealth()

        for block in current_scene.get_blocks():
            self.draw_block(block)

        self.draw_door(current_scene) 
        self.gameUIPanel.erase("orange")
        self.levelindicator.draw(current_scene.get_current_level())

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
        self.play_music(GameState.in_session)


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

        self.play_music(GameState.start_menu)

    def draw_block(self, block: Block):
        """Draws the block to the screen based on the block's coordinates.
            Attributes:
                - block: The Block object.
        """
        self.screen.blit(self.blockImage, (block.x, block.y))
    
    def draw_door(self, scene):
        """Draws the door onto the scene.
        """
        self.screen.blit(self.doorImage, (scene.door.x, scene.door.y))

    def drawButtons(self):
        """Draws the interactive UI buttons onto the screen.
        """
        for button in self.menu_buttons:
            self.screen.blit(button.renderer, button.rect)

    def updateSprite(self, current_scene):
        self.drawBackground(GameState.in_session)
        self.updateGameUIElements(current_scene)
        self.screen.blit(self.character_sprites[self.current_sprite_index],
                         (self.player_data.xPos, self.player_data.yPos))
    
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
            self.updateGameUIElements(current_scene)
            self.player_data = current_scene.player

            for i in range(self.rows):
                for j in range(self.columns):
                    self.drawBackground(GameState.in_session)
                    self.updateGameUIElements(current_scene)
                    self.character_sprites[i * self.columns + j].blit(self.sprite_sheet, (0, 0), (
                    j * self.player_data.width, i * self.player_data.height, self.player_data.width,
                    self.player_data.height))
        
            self.enemies_data = current_scene.enemies
            for enemy in self.enemies_data:
                for i in range(self.enemy_rows):
                    for j in range(self.enemy_columns):
                        self.drawBackground(GameState.in_session)
                        self.updateGameUIElements(current_scene)
                        self.character_sprites[i * self.enemy_columns + j].blit(self.sprite_sheet_mummy, (0, 0), (
                        j * enemy.width, i * enemy.height, enemy.width,
                        enemy.height))
            

            # move the character to the right if the right key is pressed
            if self.player_data.facing == Movement.right:
                # x += 1
                self.direction = "right"
                self.frame_count += 1
                if self.frame_count == self.frame_delay:
                    self.current_sprite_index = (self.current_sprite_index + 1) % self.columns          ####!!!! for changing the legs moving
                    self.frame_count = 0

            # move the character to the left if the left key is pressed

            if self.player_data.facing == Movement.left:
                # x += 1
                self.direction = "left"
                self.frame_count += 1
                if self.frame_count == self.frame_delay:
                    self.current_sprite_index = self.columns + (self.current_sprite_index + 2) % self.columns   ####!!!! for changing the legs moving
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
                self.direction = "right punch"
                self.current_sprite_index = 6
                    
            # left punch picture and code
            if  self.player_data.facing == Movement.left_punch:
                self.direction = "left punch"
                self.current_sprite_index = 7

            
            # update the current sprite based on the direction of the character
            if self.direction == "right":
                if self.current_sprite_index < self.columns:
                    self.updateSprite(current_scene)
            elif self.direction == "left":
                if self.current_sprite_index >= self.columns:
                    self.updateSprite(current_scene)
            elif self.direction == "no movement":
                if self.current_sprite_index >= self.columns:
                    self.updateSprite(current_scene)
                if self.current_sprite_index < self.columns:
                    self.updateSprite(current_scene)
            elif self.direction == "right punch" or self.direction == "left punch" or self.direction == "jump":
                self.updateSprite(current_scene)

            # move the enemy to the right if the right key is pressed
            for enemy in self.enemies_data:
                if enemy.facing == Movement.right:
                    # x += 1
                    self.direction = "right"
                    self.frame_count += 1
                    if self.frame_count == self.frame_delay:
                        self.current_sprite_index = (self.current_sprite_index + 1) % self.enemy_columns          ####!!!! for changing the legs moving
                        self.frame_count = 0

                # move the enemy to the left if the left key is pressed

                if enemy.facing == Movement.left:
                    # x += 1
                    self.direction = "left"
                    self.frame_count += 1
                    if self.frame_count == self.frame_delay:
                        self.current_sprite_index = self.enemy_columns + (self.current_sprite_index + 2) % self.enemy_columns   ####!!!! for changing the legs moving
                        self.frame_count = 0
            # update the current sprite based on the direction of the character
            if self.direction == "right":
                if self.current_sprite_index < self.enemy_columns:
                    self.updateSprite(current_scene)
            elif self.direction == "left":
                if self.current_sprite_index >= self.enemy_columns:
                    self.updateSprite(current_scene)
        elif current_scene.game_state == GameState.start_menu:
            self.drawBackground(current_scene.game_state)
            self.drawLogo()
            self.drawButtons()

    def checking_hover(self, mouse_pos: tuple):
        """check for hovering over the buttons in menue
            This method checks whether the mouse over any buttons start menu which is an array,
             Attributes:
                 - mouse_pos: A tuple containing the x and y positions of the mouse.
            """
        for button in self.menu_buttons:
            if button.rect.collidepoint(mouse_pos):
                button.setBlue()
            else:
                button.setBlack()

    def check_play_pressed(self, event):
        """Continuously checks if the Play button in the menu has been pressed, and loads the game if so.
            Attributes:
                - event: The event object in Pygame.
        """
        if self.menu_buttons[0].rect.collidepoint(event.pos):
            if not self.loadedGame:
                self.loading_screen()
                self.initialiseGameScene()
                self.initialiseGameUIElements()
    
    def play_music(self, game_state):
        """Handles music in the scene.

           Attributes:
               - game_state: The current game state.
        """

        if game_state == GameState.start_menu:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("src/view/assets/start_menu.mp3")
        elif game_state == GameState.in_session:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("src/view/assets/gamemusic.mp3")
        
        pygame.mixer.music.play(loops=-1)

    def play_sound_effect(self, sound: str):
        """Plays a sound effect.

            Attributes:
                - sound: The sound to play.
        """
        
        if sound == "punch":
            pass
            # pygame.mixer.Sound.play(self.punch_sound)
        
