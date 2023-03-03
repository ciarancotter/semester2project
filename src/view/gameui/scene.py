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

#from shared_memory_dict import SharedMemoryDict

from model.gameobjects.entity import Block
from model.gameobjects.public_enums import Movement
from model.gameobjects.public_enums import GameState
from model.gameobjects.public_enums import EnemySprite

from view.gameui.uielements import Button, TextBox, Panel
from view.gameui.healthbar import HealthBar, LevelIndicator

from model.gameobjects.game_interface import PlatformerGame
from model.aiutilities.aiutilities import generate_background, generate_monolith


class Scene:
    """A class representing the elements that should be rendered in a Pygame window.

    The Scene object is created and managed by the PlatformerGame class. Where the PlatformerGame
    class controls game state, the Scene class renders the state to the Pygame window.

    Attributes:
        game_manager: The PlatformerGame object that contains all of the game's current state data. 
    """

    def __init__(self, buttons: list[Button], background, screen):
        """Inits the Scene class.
        """
        pygame.init()
        
        self.screen = screen
        self.buttons = buttons
        self.background = background
        self.direction = "right"

        # Load the assets that should be used globally.
        bradley_base = pygame.image.load("src/view/assets/bradley.png").convert_alpha()
        logo_base = pygame.image.load("src/view/assets/logo.png")
        self.bradley = pygame.transform.scale(bradley_base, (244, 244))
        self.logo = pygame.transform.scale(logo_base, (800, 150))


    def draw_buttons(self):
        """Draws the interactive UI buttons onto the screen.
        """
        for button in self.buttons:
            self.screen.blit(button.renderer, button.rect)


    def draw_background(self):
        """Draws the background.
        """
        self.screen.blit(self.background, (0, 0))


    def draw_bradley(self):
        """Draws Bradley
        """
        bradley_rekt = self.bradley.get_rect()
        bradley_rekt.center = (640, 200)
        self.screen.blit(self.bradley, bradley_rekt)


    def draw_logo(self):
        """Draws the logo.
        """
        logo_rect = self.logo.get_rect()
        logo_rect.center = (640, 150)
        self.screen.blit(self.logo, logo_rect)


    def checking_hover(self, mouse_pos: tuple):
        """check for hovering over the buttons in menue
            This method checks whether the mouse over any buttons start menu which is an array,
             Attributes:
                 - mouse_pos: A tuple containing the x and y positions of the mouse.
            """
        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos):
                button.setBlue()
            else:
                button.setBlack()

    def draw_cursor(self, mouse_pos: tuple):
        """Draws the cursor where the mouse is or the hand is.
        """
        cursor = pygame.image.load("src/view/assets/cursor.png")
        cursor_rekt = cursor.get_rect()
        cursor_rekt.center = mouse_pos
        self.screen.blit(cursor, cursor_rekt)


    def play_music(self):
        """Handles music in the scene.
        """
        pygame.mixer.music.stop()
        pygame.mixer.music.play(loops=-1)


    def play_sound_effect(self, sound: str):
        """Plays a sound effect.

            Attributes:
                - sound: The sound to play.
        """
        
        if sound == "punch":
            pass
            # pygame.mixer.Sound.play(self.punch_sound)


class LoadingScene(Scene):
    
    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        self.text = pygame.font.SysFont("monospace", 30).render('Loading...', True, "white")
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (
                self.screen.get_width() // 2,
                self.screen.get_height() // 2
                )
        super().__init__([], None, screen)


    def update(self):
        """Draws a loading screen.
        """
        self.screen.fill("black")
        self.draw_bradley()
        self.screen.blit(self.text, self.text_rect)
        pygame.display.update()


class AboutMenuScene(Scene):

    def __init__(self, screen):
        """Inits the About menu.
        """
        pygame.init()
        self.text = None
        self.text_rect = None
        self.screen = screen


    def initialise(self):
        """Initialises some values of the About menu, but not immediately when the instance is created.
        """
        self.screen.fill("white")
        about_back_button = Button("BACK", (50, 50), 40)
        self.buttons.append(about_back_button)

        about_text = pygame.font.SysFont("monospace", 30).render('About', True, "black")
        about_text_rect = about_text.get_rect()
        about_text_rect.center = (super().screen.get_width() // 2, (super().screen.get_height() // 2) - 50)

        self.text = about_text
        self.text_rect = about_text_rect

        self.screen.blit(about_text, about_text_rect)
        super().game_manager.set_game_state(GameState.about)


    def update(self):
        """Updates the About screen.
        """
        self.screen.blit(self.text, self.text_rect)
        self.draw_buttons()


class GameScene(Scene):

    def __init__(self, game_manager: PlatformerGame, screen, loading_screen: LoadingScene):
        """Inits GameScene.
        """
        pygame.init()
        context = game_manager.get_render_ctx()
        # Integer variables
        self.rows = 3
        self.columns = 3
        self.enemy_rows = 2
        self.enemy_columns = 3
        self.frame_count = 0
        self.frame_delay = 5
        self.current_sprite_index = 0
        self.current_sprite_index_enemy = 0
        self.inscriptions = []
        self.frame_count_enemy = 0
        self.frame_count_enemy2 = 0

        # Initialising the game manager
        self.screen = screen
        self.game_manager = game_manager
        self.loading_screen = loading_screen
        self.label = GameState.in_session

        self.player = None

        # UI elements
        self.gameplay_panel = Panel(self.screen, 784, 512, 0, 0, "black")
        self.game_ui_panel = Panel(self.screen, 496, 784, 784, 0, "orange")
        self.textbox = TextBox(self.screen, 40, 25, "monospace", 18, self.game_ui_panel)
        self.levelindicator = LevelIndicator(self.screen, self.game_ui_panel)
        self.healthbar = HealthBar(self.screen, self.gameplay_panel, 100)

        self.background = None

        door_image = pygame.image.load("src/view/assets/door.png").convert_alpha()
        self.door_image = pygame.transform.scale(door_image, (56, 56))

        monolith_image = pygame.image.load("src/view/assets/monolith.png").convert_alpha()
        self.monolith_image = pygame.transform.scale(monolith_image, (56, 56))
 
        self.block_image = pygame.image.load("src/view/assets/block2.png").convert_alpha()
        self.sprite_sheet = pygame.image.load("src/view/assets/playerSprite.png").convert_alpha()
        self.sprite_sheet_mummy = pygame.image.load("src/view/assets/mummy_spritesheet.png").convert_alpha()
        self.sprite_sheet_anubis = pygame.image.load("src/view/assets/anubis_spritesheet.png").convert_alpha()
        self.sprite_sheet_horus = pygame.image.load("src/view/assets/horus_spritesheet.png").convert_alpha()
        self.sprite_sheet_sobek = pygame.image.load("src/view/assets/sobek_spritesheet.png").convert_alpha()

        # Initialises objects to None
        self.direction = "right"
        self.loaded_game = False
        self.music = pygame.mixer.music.load("src/view/assets/gamemusic.mp3")

        size = (context.player.width, context.player.height)
        self.character_sprites = [pygame.Surface(size, pygame.SRCALPHA) for i in range(self.columns * self.rows)]
        #self.player_data = context.player
        # enemy surface
        self.enemy_sprites = [pygame.Surface(size, pygame.SRCALPHA) for i in range(self.enemy_columns * self.enemy_rows)]

        # Sounds
        #self.punch_sound = pygame.mixer.Sound("src/view/assets/punch.mp3")

        # Kinect video
        #self.video = SharedMemoryDict(name='movementVideo', size=500000)


    def initialise(self):
        """Initialises some properties of the game scene.
        """
        pygame.display.set_caption("Boole Raider")
        self.loading_screen.update()
        #generate_background("ancient Egypt")
        game_background = pygame.image.load("src/view/assets/gamebg.png").convert_alpha()
        self.background = pygame.transform.scale(game_background, (784, 784))
        self.inscriptions = generate_monolith("tragic", "Egyptian")
        self.screen.fill("gold")

        self.game_manager.set_game_state(GameState.in_session)

        self.play_music()
        self.draw_background()

        self.gameplay_panel.draw()
        self.game_ui_panel.draw()
        self.textbox.draw("")
        self.healthbar.drawMaxHealth()
        self.healthbar.drawCurrentHealth()


    def draw_door(self, context):
        """Draws the door onto the scene.
        """
        self.screen.blit(
                self.door_image, 
                (
                    context.door.x,
                    context.door.y
                )
            )


    def draw_block(self, block: Block):
        """Draws the block to the screen based on the block's coordinates.
            Attributes:
                - block: The Block object.
        """
        self.screen.blit(self.block_image, (block.x, block.y))

    

    def draw_monolith(self, context):
        """Draws the monolith to the screen
        """
        self.screen.blit(
                self.monolith_image,
                (
                    context.monolith.x,
                    context.monolith.y
                )
            )


    def update_game_ui(self): 
        """Draws the UI elements onto the game.
        """
        context = self.game_manager.get_render_ctx()
        self.game_ui_panel.draw()
        for block in context.get_blocks():
            self.draw_block(block)

        self.textbox.erase()
        self.draw_door(context)
        self.draw_monolith(context)
        self.healthbar.drawMaxHealth()
        self.healthbar.drawCurrentHealth()
        self.levelindicator.draw(context.get_current_level())

        # Checks to see if we are approaching the end of the current legend.
        if context.get_current_level() == (len(self.inscriptions) - 1):
            self.inscriptions += generate_monolith("tragic", "Egyptian")

        # Writes the monolith.  
        if context.get_monolith().is_being_read is True:
            self.textbox.draw(
                    self.inscriptions[
                        context.get_current_level() - 1
                        ]
                    )
        else:
            self.textbox.draw("")


    def update_sprite(self):
        self.screen.blit(
            self.character_sprites[self.current_sprite_index],
            (self.player_data.xPos, self.player_data.yPos)
        )
    
    def enemy_selector(self, enemy):

        match enemy.choice_of_sprite:

            case EnemySprite.mummy_spritesheet:
                return self.sprite_sheet_mummy

            case EnemySprite.anubis_spritesheet:
                return self.sprite_sheet_anubis

            case EnemySprite.horus_spritesheet:
                return self.sprite_sheet_horus

            case EnemySprite.sobek_spritesheet:
                return self.sprite_sheet_sobek

            case other:
                return None


    def draw_enemy(self, context):

        for enemy in context._enemies:
            #enemy_image = self.enemy_selector(enemy)
            enemy_image = self.sprite_sheet_mummy
            
            i = self.frame_count_enemy % self.enemy_rows
            j = self.frame_count_enemy % self.enemy_columns
            self.frame_count_enemy += 1
            print(self.enemy_sprites)
            self.enemy_sprites[i * self.enemy_columns + j].blit(enemy_image, (0, 0), (
                    j * enemy.width, i * enemy.height, enemy.width,
                        enemy.height))

           
            if enemy.facing == Movement.right:
                self.enemy_direction = "right"
                self.frame_count_enemy2 += 1
                if self.frame_count_enemy2 == self.frame_delay:
                    self.current_sprite_index_enemy = (self.current_sprite_index_enemy + 1) % self.enemy_columns          ####!!!! for changing the legs moving
                    self.frame_count_enemy2 = 0
            
            if enemy.facing == Movement.left:
                    self.enemy_direction = "left"
                    self.frame_count_enemy2 += 1
                    if self.frame_count_enemy2 == self.frame_delay:
                        self.current_sprite_index_enemy = self.enemy_columns + (self.current_sprite_index_enemy + 2) % self.enemy_columns   ####!!!! for changing the legs moving
                        self.frame_count_enemy2 = 0

            if self.enemy_direction == "right":
                if self.current_sprite_index_enemy < self.enemy_columns:
                    self.screen.blit(self.enemy_sprites[self.current_sprite_index],
                                    (enemy.xPos, enemy.yPos)
                                )
            elif self.enemy_direction == "left":
                if self.current_sprite_index_enemy >= self.enemy_columns:
                    self.screen.blit(self.enemy_sprites[self.current_sprite_index],
                                    (enemy.xPos, enemy.yPos)
                                )

            """
            #move the enemy to the right if the right key is pressed
            for enemy in self.enemies_data:
                if enemy.facing == Movement.right:
                    # x += 1
                    self.enemy_direction = "right"
                    self.frame_count += 1
                    if self.frame_count == self.frame_delay:
                        self.current_sprite_index_enemy = (self.current_sprite_index_enemy + 1) % self.enemy_columns          ####!!!! for changing the legs moving
                        self.frame_count = 0

                # move the enemy to the left if the left key is pressed

                if enemy.facing == Movement.left:
                    # x += 1
                    self.enemy_direction = "left"
                    self.frame_count += 1
                    if self.frame_count == self.frame_delay:
                        self.current_sprite_index_enemy = self.enemy_columns + (self.current_sprite_index_enemy + 2) % self.enemy_columns   ####!!!! for changing the legs moving
                        self.frame_count = 0
            #update the current sprite based on the direction of the character
            if self.enemy_direction == "right":
                if self.current_sprite_index_enemy < self.enemy_columns:
                    self.updateSprite(current_scene)
            elif self.enemy_direction == "left":
                if self.current_sprite_index_enemy >= self.enemy_columns:
                    self.updateSprite(current_scene)
            """
            """
            for enemy in self.enemies_data:
                i = self.frame_count2_electric_boogaloo %self.enemy_rows
                j = self.frame_count2_electric_boogaloo % self.enemy_columns
                # print("enemy",enemy)
                # print("before corrent ")
                self.generate_enemy_sprite(enemy)
                self.frame_count2_electric_boogaloo += 1
                #for i in range(self.enemy_rows):
                #for j in range(self.enemy_columns):
                self.drawBackground(GameState.in_session)
                self.updateGameUIElements(current_scene)
                self.enemy_sprites[i * self.enemy_columns + j].blit(self.random_enemy, (0, 0), (
                j * enemy.width, i * enemy.height, enemy.width,
                enemy.height))
            """

    def draw_player(self, context):

        self.player_data = context.player

        for i in range(self.rows):
            for j in range(self.columns):
                self.character_sprites[
                        i * self.columns + j
                        ].blit(
                                self.sprite_sheet,
                                (0, 0),
                                (
                                    j * self.player_data.width,
                                    i * self.player_data.height,
                                    self.player_data.width,
                                    self.player_data.height
                                )
                            )

        # Right key -> Move Right.
        if self.player_data.facing == Movement.right:
            self.direction = "right"
            self.frame_count += 1
            if self.frame_count == self.frame_delay:
                self.current_sprite_index = (
                        self.current_sprite_index + 1
                        ) % self.columns
                self.frame_count = 0

        # Left Key -> move left.
        elif self.player_data.facing == Movement.left:
            self.direction = "left"
            self.frame_count += 1
            if self.frame_count == self.frame_delay:
                self.current_sprite_index = self.columns + (
                        self.current_sprite_index + 2
                        ) % self.columns
                self.frame_count = 0

        # Space key -> jump.
        elif self.player_data.facing == Movement.jump:
            self.direction = "jump"
            self.frame_count += 1
            if self.frame_count == self.frame_delay:
                self.current_sprite_index = self.current_sprite_index
                self.frame_count = 0

        # Idle
        elif self.player_data.facing == Movement.no_movement:
            self.direction = "no movement"
            self.current_sprite_index = self.current_sprite_index

        # Punch right!
        elif self.player_data.facing == Movement.right_punch:
            self.direction = "right punch"
            self.current_sprite_index = 6

        # Punch left!
        elif self.player_data.facing == Movement.left_punch:
            self.direction = "left punch"
            self.current_sprite_index = 7
 
        if self.direction == "right":
            if self.current_sprite_index < self.columns:
                self.update_sprite()
        elif self.direction == "left":
            if self.current_sprite_index >= self.columns:
                self.update_sprite()
        elif self.direction == "no movement":
            if self.current_sprite_index >= self.columns:
                self.update_sprite()
            if self.current_sprite_index < self.columns:
                self.update_sprite()
        elif self.direction == "right punch" or self.direction == "left punch" or self.direction == "jump":
            self.update_sprite()

    def draw_kinect(self):
        surface = pygame.surfarray.make_surface(self.video["src"])
        self.screen.blit(surface, (784, 505))


    def update(self):
        """Updates the current scene.

        This method checks whether the current scene is the start menu, or 
        the game itself. The result of this check determines what will be rendered
        in the scene.

        The drawing order should be Background -> UI Elements -> Player.
        """
        
        self.draw_background()
        self.update_game_ui()

        context = self.game_manager.get_render_ctx()
        self.draw_player(context)
        self.draw_enemy(context)


class MainMenuScene(Scene):

    def __init__(self, game_manager: PlatformerGame, screen):
        """Inits MainMenuScene.
            Attributes:
                - game_manager: The data from the model.
                - screen: The globally-defined pygame display.
        """
        pygame.init()
        self.screen = screen
        self.game_manager = game_manager
        self.label = GameState.start_menu

        # Menu buttons.
        buttons = [
            Button("PLAY", (640, 330), 85),
            Button("LEADERBOARD", (640, 430), 85),
            Button("HELP", (640, 530), 85),
            Button("ABOUT", (640, 630), 85)
        ]

        # Initialises the background, music and the parent class.
        menu_background = pygame.image.load("src/view/assets/menuBG.png").convert_alpha()
        background = pygame.transform.scale(menu_background, (1280, 784))
        pygame.mixer.music.load("src/view/assets/start_menu.mp3")
        super().__init__(buttons, background, screen)


    def initialise(self):
        """Initialises elements for the menu scene.
        """
        pygame.display.set_caption("Main Menu") 
        self.play_music()


    def check_about_pressed(self, event_pos: tuple):
        """Continuously checks if the About button in the menu has been pressed.
        """
        if self.buttons[2].rect.collidepoint(event_pos) and self.game_manager._gamestate == GameState.start_menu:
            pass # Replace with scene transition to About


    def check_play_pressed(self, event_pos: tuple, game: GameScene):
        """Continuously checks if the Play button in the menu has been pressed, and loads the game if so.
            Attributes:
                - event: The event object in Pygame.
        """
        if self.buttons[0].rect.collidepoint(event_pos) and self.game_manager._gamestate == GameState.start_menu:
            self.game_manager.set_game_state(GameState.in_session)
            game.initialise()
            # Fader(MainMenuScene, GameScene


    def update(self):
        """Updates the main menu scene.
        """
        self.draw_background()
        self.draw_logo()
        self.draw_buttons()
