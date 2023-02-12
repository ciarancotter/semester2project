
import unittest
from .entity import *
import sys 
import os
sys.path.append(os.path.abspath("./src"))
print(sys.path)
from view.imag import imag
import pygame
from game_interface import Movement
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    QUIT,
)

import unittest
from .entity import *

from view.imag import imag
import pygame
from .game_interface import Movement
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    QUIT,
)

class TestPlayer(unittest.TestCase):

    def run_after_play_button():
        # Initialize pygame
        pygame.init()

        player = Player(64,64,1000,1000)
        screen = imag(1000,1000,player.getWidth(), player.getHeight())
        # Create the screen
        clock = pygame.time.Clock()
        running = True

        # Main loop
        while running:
            """
            the game run while state of running is true,
            game can be stopped if user Quit using the exit buttom or exit through the Escape key
            """
            clock.tick(60)

            for event in pygame.event.get():
                # Check if key pressed (KEYDOWN event)
                if event.type == KEYDOWN:
                    # If the Esc key is pressed, then exit the main loop
                    if event.key == K_ESCAPE:
                        running = False
                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == QUIT:
                    running = False

            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[K_LEFT]:
                player.facing = Movement.left

            elif pressed_keys[K_RIGHT]:
                player.facing= Movement.right

            elif pressed_keys[K_SPACE]:
                player.facing= Movement.jump

            else:
                player.facing=Movement.no_movement

            player.move(player.facing, [])
            screen.create_screen()

            screen.update_xy(player)
