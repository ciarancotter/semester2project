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
import asyncio
import pygame

sys.path.append(os.path.abspath("./src"))

from shared_memory_dict import SharedMemoryDict

from model.gameobjects.entity import Block, Enemy, InvincibilityLoot, JumpLoot
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
        
        self.screen = screen
        self.buttons = buttons
        self.background = background
        self.direction = "right"

        # Load the assets that should be used globally.
        bradley_base = pygame.image.load("src/view/assets/bradley_squish.gif").convert_alpha()
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


    def play_music(self, scene: str):
        """Handles music in the scene.
        """
        pygame.mixer.music.stop()
        if scene == "menu":
            pygame.mixer.music.load("src/view/assets/start_menu.mp3")
        elif scene == "game":
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


class LoadingScene(Scene):
    
    def __init__(self, screen):
        self.screen = screen
        self.text = pygame.font.SysFont("monospace", 50, bold=True).render('LOADING...', True, "gold")
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (
                self.screen.get_width() // 2,
                self.screen.get_height() // 2
                )
        super().__init__([], None, screen)
        
        # Load the background image
        self.background = pygame.image.load("src/view/assets/loadingBG.png").convert()

    def draw_background(self):
        """Draws the background image onto the screen."""
        self.screen.blit(self.background, (0, 0))

    def update(self):
        """Draws a loading screen with a background image."""
        self.draw_background()
        self.draw_bradley()
        self.screen.blit(self.text, self.text_rect)
        pygame.display.update()


class LeaderboardMenuScene(Scene):

    def __init__(self, game_manager: PlatformerGame, screen):
        """Inits the About menu.
        """
        self.text = None
        self.text_rect = None
        self.screen = screen
        self.game_manager = game_manager
        self.label = GameState.leaderboard
        self.buttons = []

        self.loot_image = pygame.image.load("src/view/assets/loot.png")

        self.gold = (255, 215, 0)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.grey = (128, 128, 128)

        self.border_radius = 50
        self.message_radius_y = 140
        self.table_width = 1100
        self.table_height = 500
        self.border_radius_table_x = 90
        self.border_radius_table_y = 200
        self.distance_between_lines = 40
        self.header_border = 35
        self.border_thickness = 2
        self.border_line_distance = 12
        self.values_start_y_position = 85

        self.border_color = (self.white)
        self.line_color = (self.grey)

        # Define high scores list
        self.high_scores = []

        self.leaderboard = game_manager.return_scores()
        for name in self.leaderboard["scores"]:
            self.user_name = name
            self.score = self.leaderboard["scores"][name]
            self.high_scores.append({'name': self.user_name, 'score': self.score},)

        # Sort high scores list by score value
        self.high_scores = sorted(self.high_scores, key=lambda x: x['score'], reverse=True)

    def _render(self):
        '''Renders the Leaderboard to the screen.
        '''
        self.screen.fill(self.gold)

        ### HEADER
        leaderboard_text = pygame.font.SysFont("monospace", 50, bold=True).render('Leaderboard', True, self.black)
        leaderboard_text_rect = leaderboard_text.get_rect()
        leaderboard_text_rect.center = (self.screen.get_width() // 2, self.border_radius)

        self.text = leaderboard_text
        self.text_rect = leaderboard_text_rect

        self.screen.blit(leaderboard_text, leaderboard_text_rect)

        ### TEXTBOX 
        message_surface = pygame.font.SysFont("monospace", 40, bold=True).render("Well done you made the top 10!!", True, self.black)
        leaderboard_message_rect = message_surface.get_rect()
        leaderboard_message_rect.center = (self.screen.get_width() // 2, self.message_radius_y)

        self.message = message_surface
        self.message_rect = leaderboard_message_rect

        self.screen.blit(message_surface, leaderboard_message_rect)

        ### TABLE
        header_font = pygame.font.SysFont("monospace", 30, bold=True)
        body_font = pygame.font.SysFont("monospace", 28)
        leaderboard_surface = pygame.Surface((self.table_width, self.table_height))
        leaderboard_surface.fill((self.black))

        # Render headings onto Pygame surface
        rank_heading = header_font.render('Rank', True, (self.white))
        name_heading = header_font.render('Name', True, (self.white))
        score_heading = header_font.render('Score', True, (self.white))
        leaderboard_surface.blit(rank_heading, (self.border_radius_table_x - self.header_border, self.header_border))
        leaderboard_surface.blit(name_heading, (self.table_width//4, self.header_border))
        leaderboard_surface.blit(score_heading, (self.table_width//4 * 3, self.header_border))

        # Draw border and lines on leaderboard surface
        pygame.draw.rect(leaderboard_surface, self.border_color, (self.border_line_distance, self.border_line_distance, self.table_width-25, self.table_height-25), self.border_thickness)
        for i in range(1, 11):
            pygame.draw.line(leaderboard_surface, self.line_color, (self.border_line_distance + self.border_thickness, self.distance_between_lines + i * self.distance_between_lines), (self.table_width - self.border_line_distance - self.border_thickness*2, self.distance_between_lines + i * self.distance_between_lines), 2)

        # draw the vertical lines
        pygame.draw.line(leaderboard_surface, self.line_color, (self.table_width//6, self.border_line_distance + self.border_thickness), (self.table_width//6, self.table_height - self.border_line_distance - self.border_thickness), self.border_thickness)
        pygame.draw.line(leaderboard_surface, self.line_color, (self.table_width//3 * 2, self.border_line_distance + self.border_thickness), (self.table_width//3 * 2, self.table_height - self.border_line_distance - self.border_thickness), self.border_thickness)

        for i, score in enumerate(self.high_scores):
            if i < 10:
                rank_text = body_font.render(str(i+1), True, (self.white))
                name_text = body_font.render(score['name'], True, (self.white))
                score_text = body_font.render(str(score['score']), True, (self.white))
                leaderboard_surface.blit(rank_text, (self.border_radius_table_x - self.header_border, self.values_start_y_position + i * self.distance_between_lines))
                leaderboard_surface.blit(name_text, (self.table_width//4, self.values_start_y_position + i * self.distance_between_lines))
                leaderboard_surface.blit(score_text, (self.table_width//4 * 3, self.values_start_y_position + i * self.distance_between_lines))

        # Blit leaderboard surface onto Pygame window
        self.screen.blit(leaderboard_surface, (self.border_radius_table_x, self.border_radius_table_y))
        self.screen.blit(self.loot_image, (300, 15))
        self.screen.blit(self.loot_image, (850, 15))

    def initialise(self):
        """Initialises some values of the Leaderboard menu, but not immediately when the instance is created.
        """
        leaderboard_back_button = Button("BACK", (50, 50), 40)
        self.buttons.append(leaderboard_back_button)
        
        self._render()


    def update(self):
        """Updates the About screen.
        """
        self._render()
        self.draw_buttons()


    def check_back_pressed(self, event_pos: tuple, main_menu_scene: Scene):
        """Continuously checks if the Back button in the menu has been pressed, and returns to main menu.
            Attributes:
                - event: The event object in Pygame.
        """
        if self.game_manager._gamestate == GameState.leaderboard and self.buttons[0].rect.collidepoint(event_pos):
            self.game_manager.set_game_state(GameState.start_menu)
            main_menu_scene.initialise()


class HelpMenuScene(Scene):

    def __init__(self, game_manager: PlatformerGame, screen):
        """Inits the About menu.
        """
        self.text = None
        self.text_rect = None
        self.screen = screen
        self.game_manager = game_manager
        self.label = GameState.about
        self.buttons = []

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.gold = (255, 215, 0)

        ### load assets

        self.loot_image = pygame.image.load("src/view/assets/loot.png")
        self.jump_boost_image = pygame.image.load("src/view/assets/jump_boost.png")
        self.health_boost_image = pygame.image.load("src/view/assets/health_boost.png")
        self.invincibility_image = pygame.image.load("src/view/assets/invincibility.png")
        self.monolith_image = pygame.image.load("src/view/assets/monolith.png")
        self.door_image = pygame.image.load("src/view/assets/door.png")

        self.loot_description = "Loot"
        self.jump_boost_description = "Jump Boost"
        self.health_boost_description = "Health Boost"
        self.invincibility_description = "Shield"
        self.monolith_description = "Stand by this monolith to continue the story."
        self.door_description = "Get to the door and walk through to complete each level."

        self.walk_left_image = pygame.image.load("src/view/assets/help_sprite_walk_left.png")
        self.walk_right_image = pygame.image.load("src/view/assets/help_sprite_walk_right.png")
        self.punch_left_image =  pygame.image.load("src/view/assets/help_sprite_punch_left.png")
        self.punch_right_image =  pygame.image.load("src/view/assets/help_sprite_punch_right.png")

        self.walk_left_description = "To walk left"
        self.walk_right_description = "To walk right"
        self.punch_left_description = "To punch left"
        self.punch_right_description = "To punch right"

        self.enemy1 = pygame.image.load("src/view/assets/help_enemy_1.png")
        self.enemy2 = pygame.image.load("src/view/assets/help_enemy_2.png")
        self.enemy3 = pygame.image.load("src/view/assets/help_enemy_3.png")
        self.enemy4 = pygame.image.load("src/view/assets/help_enemy_4.png")

        # Load the spritesheet images and set the size of each sprite in the spritesheet
        self.spritesheets = [
            (pygame.image.load("src/view/assets/help_screen/Bradley_twistleft_spritesheet.png"), 200, 300),
            (pygame.image.load("src/view/assets/help_screen/Patrick_twistright_spritesheet.png"), 200, 300),
            (pygame.image.load("src/view/assets/help_screen/Shaza_select_spritesheet.png"), 200, 300),
            (pygame.image.load("src/view/assets/help_screen/Niamh_punchleft_spritesheet.png"), 200, 300),
            (pygame.image.load("src/view/assets/help_screen/Sam_punchright_spritesheet.png"), 200, 300),
            (pygame.image.load("src/view/assets/help_screen/Ciaran_jump_spritesheet.png"), 200, 300)
        ]

        # Define the rect object for each sprite in the spritesheets
        self.sprite_rects = [
            [
                pygame.Rect((x, 0), (width, height)) for x in range(0, 800, width)
            ] for _, width, height in self.spritesheets
        ]

        # Set the initial sprite index for each spritesheet to 0
        self.sprite_indices = [0] * len(self.spritesheets)

        self.frame_count = 0


    def _render(self):
        '''Renders the help screen
        '''
        self.screen.fill((2,0,121))

        ### ITEMS BOX
        square_position = (0, 50)
        square_size = (600, 200)
        border_radius = 20
        pygame.draw.rect(self.screen, (255, 215, 0), (square_position, square_size), border_radius=border_radius)

        border_position = (square_position[0] - 5, square_position[1] - 5)
        border_size = (square_size[0] + 10, square_size[1] + 10)
        border_radius = 20
        pygame.draw.rect(self.screen, (0, 0, 0), (border_position, border_size), 5, border_radius=border_radius)

        font = pygame.font.SysFont("monospace", 40, bold=True)
        text = "COLLECT YOUR ITEMS!"
        text_surface = font.render(text, True, self.black, self.gold)
        text_rect = text_surface.get_rect()
        text_rect.center = ((square_position[0] + square_size[0]) // 2, square_position[1] + 50)
        self.screen.blit(text_surface, text_rect)

        font = pygame.font.SysFont("monospace", 20, bold=True)
        self.screen.blit(self.loot_image, (0, 120))
        loot_text = font.render(self.loot_description, True, (0,0,0))
        self.screen.blit(loot_text, (40, 190))

        self.screen.blit(self.jump_boost_image, (165, 120))
        jump_boost_text = font.render(self.jump_boost_description, True, (0,0,0))
        self.screen.blit(jump_boost_text, (170, 190))

        self.screen.blit(self.health_boost_image, (350, 120))
        health_boost_text = font.render(self.health_boost_description, True, (0,0,0))
        self.screen.blit(health_boost_text, (320, 190))

        self.screen.blit(self.invincibility_image, (500, 120))
        invincibility_text = font.render(self.invincibility_description, True, (0,0,0))
        self.screen.blit(invincibility_text, (500, 190))

        ### DOOR AND MONOLITH BOX
        square_position = (0, 300)
        square_size = (600, 228)
        border_radius = 20
        pygame.draw.rect(self.screen, (255, 215, 0), (square_position, square_size), border_radius=border_radius)

        border_position = (square_position[0] - 5, square_position[1] - 5)
        border_size = (square_size[0] + 10, square_size[1] + 10)
        border_radius = 20
        pygame.draw.rect(self.screen, (0, 0, 0), (border_position, border_size), 5, border_radius=border_radius)

        font = pygame.font.SysFont("monospace", 13, bold=True)

        self.screen.blit(self.monolith_image, (30, 320))
        monolith_text = font.render(self.monolith_description, True, (0,0,0))
        self.screen.blit(monolith_text, (140, 350))

        self.screen.blit(self.door_image, (0, 400))
        door_text = font.render(self.door_description, True, (0,0,0))
        self.screen.blit(door_text, (140, 450))

        ### ENEMIES BOX
        square_position = (0, 600)
        square_size = (600, 150)
        border_radius = 20
        pygame.draw.rect(self.screen, (255, 215, 0), (square_position, square_size), border_radius=border_radius)

        border_position = (square_position[0] - 5, square_position[1] - 5)
        border_size = (square_size[0] + 10, square_size[1] + 10)
        border_radius = 20
        pygame.draw.rect(self.screen, (0, 0, 0), (border_position, border_size), 5, border_radius=border_radius)

        font = pygame.font.SysFont("monospace", 30, bold=True)
        text = "DONT LET THEM GET TO YOU!"
        text_surface = font.render(text, True, self.black, self.gold)
        text_rect = text_surface.get_rect()
        text_rect.center = ((square_position[0] + square_size[0]) // 2, square_position[1] + 50)
        self.screen.blit(text_surface, text_rect)

        self.screen.blit(self.enemy1, (100, 670))
        self.screen.blit(self.enemy2, (200, 670))
        self.screen.blit(self.enemy3, (300, 670))
        self.screen.blit(self.enemy4, (400, 670))

        ### MOVEMENTS BOX
        square_position = (700, 0)
        square_size = (580, 780)
        
        pygame.draw.rect(self.screen, (255, 215, 0), (square_position, square_size))

        border_position = (square_position[0] - 5, square_position[1] - 5)
        border_size = (square_size[0] + 10, square_size[1] + 10)
        
        pygame.draw.rect(self.screen, (0, 0, 0), (border_position, border_size), 5)

        font = pygame.font.SysFont("monospace", 40, bold=True)
        text = "MOVEMENTS"
        text_surface = font.render(text, True, self.black, self.gold)
        text_rect = text_surface.get_rect()
        text_rect.center = (square_position[0] + square_size[0] // 2, square_position[1] + 50)
        self.screen.blit(text_surface, text_rect)

        #position of each row of spritesheets
        rows = [
            (700, 75), 
            (700, 430),
        ]
        
        # iterate through the spritesheets list and keep track of the index of each one
        for i, (spritesheet, width, height) in enumerate(self.spritesheets): #keep track of index sprite within spritesheets
            sprite_index = self.sprite_indices[i]
            sprite_rect = self.sprite_rects[i][sprite_index]
            sprite = spritesheet.subsurface(sprite_rect)
            row_x, row_y = rows[i // 3]
            sprite_x = row_x + (i % 3) * 200
            sprite_y = row_y
            self.screen.blit(sprite, (sprite_x, sprite_y))
            if self.frame_count % 17 == 0:
                self.sprite_indices[i] = (sprite_index + 1) % len(self.sprite_rects[i])
        
        self.frame_count +=1

        font = pygame.font.SysFont("monospace", 15, bold=True)

        self.screen.blit(self.walk_left_image, (700, 350))
        walk_left_text = font.render(self.walk_left_description, True, (0,0,0))
        self.screen.blit(walk_left_text, (740, 410))

        self.screen.blit(self.walk_right_image, (910, 350))
        walk_right_text = font.render(self.walk_right_description, True, (0,0,0))
        self.screen.blit(walk_right_text, (940, 410))
        
        self.screen.blit(self.punch_right_image, (700, 720))
        punch_left_text = font.render(self.punch_left_description, True, (0,0,0))
        self.screen.blit(punch_left_text, (760, 750))

        self.screen.blit(self.punch_left_image, (910, 720))
        punch_left_text = font.render(self.punch_right_description, True, (0,0,0))
        self.screen.blit(punch_left_text, (960, 750))

        select_text = font.render("Select", True, (0,0,0))
        self.screen.blit(select_text, (1160, 410))

        jump_text = font.render("Jump", True, (0,0,0))
        self.screen.blit(jump_text, (1170, 750))

    def initialise(self):
        """Initialises some values of the Help menu, but not immediately when the instance is created.
        """
        help_back_button = Button("BACK", (50, 50), 40)
        self.buttons.append(help_back_button)
        self._render()

    def update(self):
        """Updates the About screen.
        """
        self._render()
        self.draw_buttons()


    def check_back_pressed(self, event_pos: tuple, main_menu_scene: Scene):
        """Continuously checks if the Back button in the menu has been pressed, and returns to main menu.
            Attributes:
                - event: The event object in Pygame.
        """
        if self.game_manager._gamestate == GameState.help_screen and self.buttons[0].rect.collidepoint(event_pos):
            self.game_manager.set_game_state(GameState.start_menu)
            main_menu_scene.initialise()


class AboutMenuScene(Scene):

    def __init__(self, game_manager: PlatformerGame, screen):
        """Inits the About menu.
        """
        self.text = None
        self.text_rect = None
        self.screen = screen
        self.game_manager = game_manager
        self.label = GameState.about
        self.buttons = []

        self.background_image = pygame.image.load("src/view/assets/aboutBG.png")
        self.background_rect = self.background_image.get_rect()

        self.logo = pygame.image.load("src/view/assets/logo.png")
        self.logo = pygame.transform.scale(self.logo, (800, 150))

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.gold = (255, 215, 0)

        self.bradley = pygame.image.load("src/view/assets/profiles/bradleyAbout.png")
        self.niamh = pygame.image.load("src/view/assets/profiles/niamhAbout.png")
        self.ciaran = pygame.image.load("src/view/assets/profiles/ciaranAbout.png")
        self.samina = pygame.image.load("src/view/assets/profiles/saminaAbout.png")
        self.shaza = pygame.image.load("src/view/assets/profiles/shazaAbout.png")
        self.patrick = pygame.image.load("src/view/assets/profiles/patrickAbout.png")

        self.bradley_description="Bradley Harris"
        self.samina_description="Samina Arshad"
        self.niamh_description="Niamh Connolly"
        self.shaza_description="Shaza"
        self.ciaran_description="Ciaran Cotter"
        self.patrick_description="Patrick Lenhian"

        self.bradley_role="Machine Vision Developer"
        self.samina_role="Developer and Artist"
        self.niamh_role="Pygame expert"
        self.shaza_role="Pygame Developer"
        self.ciaran_role="Ai and View specialist"
        self.patrick_role="System Architect"

    def _render(self):
        '''Renders the about menu
        '''
        self.screen.blit(self.background_image, self.background_rect)

        # Draw a gold square with rounded corners under the developers
        square_position = (0, 190)
        square_size = (700, 500)
        border_radius = 20
        pygame.draw.rect(self.screen, (self.gold), (square_position, square_size), border_radius=border_radius)

        # Add text to the gold square
        font = pygame.font.SysFont("monospace", 72, bold=True)
        text = "MEET THE TEAM"
        text_surface = font.render(text, True, self.black, self.gold)
        text_rect = text_surface.get_rect()
        text_rect.center = ((square_position[0] + square_size[0]) // 2, square_position[1] + 50)
        self.screen.blit(text_surface, text_rect)

        # Draw a black border around the square
        border_position = (square_position[0] - 5, square_position[1] - 5)
        border_size = (square_size[0] + 10, square_size[1] + 10)
        border_radius = 20
        pygame.draw.rect(self.screen, (self.black), (border_position, border_size), 5, border_radius=border_radius)

        # Define the position and size of the text box
        text_box_position = (800, 190)
        text_box_size = (410, 300) 


        # Define the font and color for the text
        font = pygame.font.SysFont("monospace", 18, bold=True)
        smallfont = pygame.font.SysFont("monospace", 14, bold=True)

        # Create a surface with the desired text
        long_sentence = "Welcome to Boole Raider! This is a camera recognition game which allows you to lead the character in the game and go through the levels with your own movements! We are a group of computer scientist students that have created this game for their software engineering project at UCC in the college year of 2022-2023. Click HELP on the main menu to learn how to play!"
        text_surface = font.render(long_sentence, True, self.black)

        # Wrap the text in a box of 400px width
        lines = []
        while long_sentence:
            i = 1
            # Find the maximum number of characters that fit in the 400px width
            while font.size(long_sentence[:i])[0] < 400 and i < len(long_sentence):
                i += 1
            # If the entire sentence fits within the 400px width, add it as a line
            if i == len(long_sentence):
                lines.append(long_sentence)
                long_sentence = ""
            else:
                # Find the last space within the 400px width to split the line
                if " " in long_sentence[:i]:
                    i = long_sentence[:i].rfind(" ") + 1
                # Add the line to the list
                lines.append(long_sentence[:i])
                long_sentence = long_sentence[i:]

        # Create a surface for the text box with a gold background
        text_box_surface = pygame.Surface(text_box_size)
        text_box_surface.fill(self.gold)

        # Blit the wrapped text surface onto the text box surface
        y = 10
        for line in lines:
            text_surface = font.render(line, True, self.black, self.gold)
            text_box_surface.blit(text_surface, (10, y))
            y += text_surface.get_height() + 5

        # Create a surface for the black border
        border_surface = pygame.Surface((text_box_size[0] + 10, text_box_size[1] + 10))
        border_surface.fill(self.black)

        # Draw the gold text box on top of the border surface
        border_surface.blit(text_box_surface, (5, 5))

        # Draw the black border with rounded corners on top of the gold text box
        border_rect = pygame.draw.rect(border_surface, self.black, (0, 0, text_box_size[0]+10, text_box_size[1]+10), 5, border_radius=10)

        # Blit the border surface onto the main window surface
        self.screen.blit(border_surface, text_box_position)

        # draw item images and descriptions
        font = pygame.font.SysFont("monospace", 24, bold=True)
        self.screen.blit(self.bradley, (0, 280))
        bradley_text = font.render(self.bradley_description, True, (0,0,0))
        self.screen.blit(bradley_text, (120, 350))
        bradley_text2 = smallfont.render(self.bradley_role, True, (0,0,0))
        self.screen.blit(bradley_text2, (120, 380))

        self.screen.blit(self.niamh, (0, 420))
        niamh_text = font.render(self.niamh_description, True, (0,0,0))
        self.screen.blit(niamh_text, (120, 470))
        niamh_text2 = smallfont.render(self.niamh_role, True, (0,0,0))
        self.screen.blit(niamh_text2, (120, 500))

        self.screen.blit(self.ciaran, (0, 540))
        ciaran_text = font.render(self.ciaran_description, True, (0,0,0))
        self.screen.blit(ciaran_text, (120, 600))
        ciaran_text2 = smallfont.render(self.ciaran_role, True, (0,0,0))
        self.screen.blit(ciaran_text2, (120, 630))

        self.screen.blit(self.samina, (320, 300))
        samina_text = font.render(self.samina_description, True, (0,0,0))
        self.screen.blit(samina_text, (450, 350))
        samina_text2 = smallfont.render(self.samina_role, True, (0,0,0))
        self.screen.blit(samina_text2, (450, 380))

        self.screen.blit(self.shaza, (320, 420))
        shaza_text = font.render(self.shaza_description, True, (0,0,0))
        self.screen.blit(shaza_text, (450, 470))
        shaza_text2 = smallfont.render(self.shaza_role, True, (0,0,0))
        self.screen.blit(shaza_text2, (450, 500))

        self.screen.blit(self.patrick, (320, 540))
        patrick_text = font.render(self.patrick_description, True, (0,0,0))
        self.screen.blit(patrick_text, (450, 600))
        patrick_text2 = smallfont.render(self.patrick_role, True, (0,0,0))
        self.screen.blit(patrick_text2, (450, 630))
        

        logo_x_pos = (self.screen.get_width() - self.logo.get_width()) // 2

        self.screen.blit(self.logo, (logo_x_pos, 20))

    def initialise(self):
        """Initialises some values of the About menu, but not immediately when the instance is created.
        """
        about_back_button = Button("BACK", (50, 50), 40)
        self.buttons.append(about_back_button)
        self._render()

    def update(self):
        """Updates the About screen.
        """
        self._render()
        self.draw_buttons()


    def check_back_pressed(self, event_pos: tuple, main_menu_scene: Scene):
        """Continuously checks if the Back button in the menu has been pressed, and returns to main menu.
            Attributes:
                - event: The event object in Pygame.
        """
        if self.game_manager._gamestate == GameState.about and self.buttons[0].rect.collidepoint(event_pos):
            self.game_manager.set_game_state(GameState.start_menu)
            main_menu_scene.initialise()



class GameScene(Scene):

    def __init__(self, game_manager: PlatformerGame, screen, loading_screen: LoadingScene, KINECT: bool):
        """Inits GameScene.
        """
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
        self.updated_new_level_bg: bool = False

        # UI elements
        self.gameplay_panel = Panel(self.screen, 784, 512, 0, 0, "black")
        self.game_ui_panel = Panel(self.screen, 496, 784, 784, 0, "orange")
        self.textbox = TextBox(self.screen, 40, 25, "monospace", 18, self.game_ui_panel)
        self.levelindicator = LevelIndicator(self.screen, self.game_ui_panel)
        self.healthbar = HealthBar(self.screen, self.gameplay_panel, context.player)

        self.background = None

        door_image = pygame.image.load("src/view/assets/door.png").convert_alpha()
        self.door_image = pygame.transform.scale(door_image, (56, 56))

        monolith_image = pygame.image.load("src/view/assets/monolith.png").convert_alpha()
        self.monolith_image = pygame.transform.scale(monolith_image, (56, 56))
 
        self.block_image = pygame.image.load("src/view/assets/block2.png").convert_alpha()
        self.invincibility_image = pygame.image.load("src/view/assets/invincibility.png").convert_alpha()
        self.jump_image = pygame.image.load("src/view/assets/jump_boost.png").convert_alpha()
        self.sprite_sheet = pygame.image.load("src/view/assets/playerSprite.png").convert_alpha()
        self.sprite_sheet_mummy = pygame.image.load("src/view/assets/mummy_spritesheet.png").convert_alpha()
        self.sprite_sheet_anubis = pygame.image.load("src/view/assets/anubis_spritesheet.png").convert_alpha()
        self.sprite_sheet_horus = pygame.image.load("src/view/assets/horus_spritesheet.png").convert_alpha()
        self.sprite_sheet_sobek = pygame.image.load("src/view/assets/sobek_spritesheet.png").convert_alpha()

        # Initialises objects to None
        self.direction = "right"
        self.loaded_game = False
        self.last_saved_level = 1

        size = (context.player.width, context.player.height)
        self.character_sprites = [pygame.Surface(size, pygame.SRCALPHA) for i in range(self.columns * self.rows)]
        self.enemy_sufaces = []

        # Sounds
        #self.punch_sound = pygame.mixer.Sound("src/view/assets/punch.mp3")

        # Kinect video
        if KINECT:
            self.video = SharedMemoryDict(name='movementVideo', size=500000)

    async def load_many_backgrounds(self):
        tasks = [
                asyncio.create_task(generate_background("Ancient Egypt", 1)),
                asyncio.create_task(generate_background("Ancient Egypt", 2)),
                asyncio.create_task(generate_background("Ancient Egypt", 3)),
                asyncio.create_task(generate_background("Ancient Egypt", 4)),
                asyncio.create_task(generate_background("Ancient Egypt", 5))
                ]
        await asyncio.gather(*tasks)
    
    def initialise(self):
        """Initialises some properties of the game scene.
        """
        pygame.display.set_caption("Boole Raider")
        self.loading_screen.update()
        # asyncio.run(self.load_many_backgrounds())  # Parallel asset downloading
        
        #generate_background("Ancient Egypt")
        game_background = pygame.image.load("src/view/assets/gamebg1.png").convert_alpha()
        self.background = pygame.transform.scale(game_background, (784, 784))
        self.inscriptions = generate_monolith("tragic", "Egyptian")
        self.screen.fill("gold")

        self.game_manager.set_game_state(GameState.in_session)

        self.play_music("game")
        self.draw_background()

        self.gameplay_panel.draw()
        self.game_ui_panel.draw()
        self.textbox.draw("")


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
    
    def draw_loot(self, context):
        """Draws loot to the screen
        """
        if type(context.loot) == JumpLoot:
            self.screen.blit(
                self.jump_image,
                (
                    context.loot.x,
                    context.loot.y
                )
            )
        elif type(context.loot) == InvincibilityLoot:
            self.screen.blit(
                self.invincibility_image,
                (
                    context.loot.x,
                    context.loot.y
                )
            )

    def update_game_ui(self):
        """Draws the UI elements onto the game.
        """
        context = self.game_manager.get_render_ctx()

        # Checks to see if we need to update the current level's background.
        #if self.last_saved_level != context.get_current_level():
            #background_path = 'src/view/assets/gamebg' + str(context.get_current_level()) + '.png'
            #game_background = pygame.image.load(background_path).convert_alpha()
            #self.background= pygame.transform.scale(game_background, (784, 784))
            #self.last_saved_level = context.get_current_level()

        self.game_ui_panel.draw()
        for block in context.get_blocks():
            self.draw_block(block)

        self.textbox.erase()
        self.draw_door(context)
        self.draw_monolith(context)
        self.draw_loot(context)
        self.healthbar.draw_health(context.player)
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


    def display_player(self):
        self.screen.blit(
            self.character_sprites[self.current_sprite_index],
            (self.player_data.xPos, self.player_data.yPos)
        )

    def display_enemies(self,ctx):
        """displays the enemys on the screen.

        displays each enemy on the screen using the contexts list of enemies 
        and the enemy surfaces which contain a list of surfaces to be drawn on.
        """
        for i,enemy in enumerate(ctx.enemies):
            self.screen.blit(
                self.enemy_sufaces[i][self.current_sprite_index_enemy],
                (enemy.x, enemy.y)
            )

    
    def enemy_selector(self, enemy: Enemy):

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
        if len(self.enemy_sufaces)<len(context.enemies) :
            for i in range(len(context.enemies)-len(self.enemy_sufaces)):
                self.enemy_sufaces.append([pygame.Surface(context.entity_size, pygame.SRCALPHA) for i in range(self.enemy_columns * self.enemy_rows)])
        if len(context.enemies)<len(self.enemy_sufaces):
            for i in range(len(self.enemy_sufaces)-len(context.enemies)):
                self.enemy_sufaces.pop()


        for e,enemy in enumerate(context.enemies):
            enemy_image = self.enemy_selector(enemy)
            i = 0
            j = 0
            #i = self.frame_count_enemy % self.enemy_rows
            #j = self.frame_count_enemy % self.enemy_columns
            self.frame_count_enemy += 1

            self.enemy_sufaces[e][i * self.enemy_columns + j].blit(enemy_image, (0, 0), (
                    j * enemy.width, i * enemy.height, enemy.width,
                        enemy.height))
            # the bellow does nothing it is brocken
            match enemy.facing:
                case Movement.right:
                    self.enemy_direction = "right"
                    self.frame_count_enemy2 += 1
                    if self.frame_count_enemy2 == self.frame_delay:
                        self.current_sprite_index_enemy = (self.current_sprite_index_enemy + 1) % self.enemy_columns          ####!!!! for changing the legs moving
                        self.frame_count_enemy2 = 0
                case Movement.left:
                    self.enemy_direction = "left"
                    self.frame_count_enemy2 += 1
                    if self.frame_count_enemy2 == self.frame_delay:
                        self.current_sprite_index_enemy = self.enemy_columns + (self.current_sprite_index_enemy + 2) % self.enemy_columns   ####!!!! for changing the legs moving
                        self.frame_count_enemy2 = 0
        
        # TODO:fix this 

        self.current_sprite_index_enemy = 0
        self.frame_count_enemy2 = 0
        # end TODO
        self.display_enemies(context)

    def draw_player(self, context):
        self.player_data = context.player
        for i in range(self.rows):
            for j in range(self.columns):
                self.character_sprites[i * self.columns + j].blit(
                        self.sprite_sheet, (0, 0),
                        (j * self.player_data.width, i * self.player_data.height,
                            self.player_data.width, self.player_data.height)
                        )

        match self.player_data.facing:
            # Right key -> Move Right.
            case Movement.right:
                self.frame_count += 1
                if self.frame_count == self.frame_delay:
                    self.current_sprite_index = (
                            self.current_sprite_index + 1
                            ) % self.columns
                    self.frame_count = 0
            # Left Key -> move left.
            case Movement.left:
                self.frame_count += 1
                if self.frame_count == self.frame_delay:
                    self.current_sprite_index = self.columns + (
                            self.current_sprite_index + 2
                            ) % self.columns
                    self.frame_count = 0
            # Space key -> jump.
            case Movement.jump:
                self.direction = "jump"
                self.frame_count += 1
                if self.frame_count == self.frame_delay:
                    self.current_sprite_index = self.current_sprite_index
                    self.frame_count = 0
            # Idle
            case Movement.no_movement:
                self.current_sprite_index = self.current_sprite_index
            # Punch right!
            case Movement.right_punch:
                self.current_sprite_index = 6
            # Punch left!
            case Movement.left_punch:
                self.current_sprite_index = 7
 
        self.display_player()


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

class GameOverScene(Scene):

    def __init__(self, game_manager: PlatformerGame, screen):
        """Inits the About menu.
        """
        self.text = None
        self.text_rect = None
        self.screen = screen
        self.game_manager = game_manager
        self.label = GameState.game_over
        self.buttons = []

    def _render(self):
        '''Renders the Leaderboard to the screen.
        '''
        self.leaderboard = self.game_manager.return_scores()

        square_position = (245, 280)
        square_size = (600, 150)
        border_radius = 20
        pygame.draw.rect(self.screen, (100, 100, 100), (square_position, square_size), border_radius=border_radius)


        over_text = pygame.font.SysFont("monospace", 86, True).render('GAME OVER', True, "red")
        over_text_rect = over_text.get_rect()
        over_text_rect.center = ((self.screen.get_width() // 2) - 100, (self.screen.get_height() // 2) - 50)

        name = "Username: %s" %(self.leaderboard["most recent player"])
        name_text = pygame.font.SysFont("monospace", 32, True).render(name, True, "white")
        name_text_rect = name_text.get_rect()
        name_text_rect.center = ((self.screen.get_width() // 2) - 100, (self.screen.get_height() // 2) )

        self.screen.blit(over_text, over_text_rect)
        self.screen.blit(name_text, name_text_rect)


    def update(self):
        """Updates the About screen.
        """
        self._render()
        self.draw_buttons()


class MainMenuScene(Scene):

    def __init__(self, game_manager: PlatformerGame, screen):
        """Inits MainMenuScene.
            Attributes:
                - game_manager: The data from the model.
                - screen: The globally-defined pygame display.
        """
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

        super().__init__(buttons, background, screen)


    def initialise(self):
        """Initialises elements for the menu scene.
        """
        pygame.display.set_caption("Main Menu") 
        self.play_music("menu")

    def check_play_pressed(self, event_pos: tuple, game: GameScene):
        """Continuously checks if the Play button in the menu has been pressed, and loads the game if so.
            Attributes:
                - event: The event object in Pygame.
        """
        if self.buttons[0].rect.collidepoint(event_pos) and self.game_manager._gamestate == GameState.start_menu:
            self.game_manager.set_game_state(GameState.in_session)
            game.initialise()
            # Fader(MainMenuScene, GameScene

    def check_leaderboard_pressed(self, event_pos: tuple, leaderboard: LeaderboardMenuScene):
        """Continuously checks if the leaderboard button in the menu has been pressed.
        """
        if self.buttons[1].rect.collidepoint(event_pos) and self.game_manager._gamestate == GameState.start_menu:
            self.game_manager.set_game_state(GameState.leaderboard)
            leaderboard.initialise()

    def check_help_pressed(self, event_pos: tuple, help: HelpMenuScene):
        """Continuously checks if the help button in the menu has been pressed.
        """
        if self.buttons[2].rect.collidepoint(event_pos) and self.game_manager._gamestate == GameState.start_menu:
            self.game_manager.set_game_state(GameState.help_screen)
            help.initialise()

    def check_about_pressed(self, event_pos: tuple, about: AboutMenuScene):
        """Continuously checks if the About button in the menu has been pressed.
        """
        if self.buttons[3].rect.collidepoint(event_pos) and self.game_manager._gamestate == GameState.start_menu:
            self.game_manager.set_game_state(GameState.about)
            about.initialise()
            

    def update(self):
        """Updates the main menu scene.
        """
        self.draw_background()
        self.draw_logo()
        self.draw_buttons()
