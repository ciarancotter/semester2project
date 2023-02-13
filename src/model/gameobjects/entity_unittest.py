import os
import sys 
import pygame
import unittest

from entity import Player
from entity import Block
from entity import Entity
from public_enums import Movement






class TestPlayer(unittest.TestCase):
    def test_collide(self):
        """ check that the player. collide is working """
        play = Player(50,50,1000,1000)
        blocks = [Block(Entity(503,553,32,32,True))]
        play.move(Movement.no_movement,blocks)
        print("xPosition",play.yPos)
        collide_test = play.collideTop(blocks)
        self.assertTrue(collide_test,"not correct")
    def test_update(self):
        testPlayer = Player(50,50,1000,1000)
        testPlayer.move(Movement.no_movement,[])
        self.assertEqual(testPlayer.yPos,504,"gravity not working")
    def testPlatform(self):
        testPlayer = Player(50,50,1000,1000)
        blocks = [Block(Entity(503,550,32,32,True))]
        testPlayer.move(Movement.no_movement,blocks)
        testPlayer.move(Movement.no_movement,blocks)
        testPlayer.move(Movement.no_movement,blocks)
        self.assertEqual(testPlayer.yPos,504,"player has moved through a solid object")
    def testMove(self):
        testPlayer = Player(50,50,1000,1000)
        testPlayer.move(Movement.right,[])
        self.assertEqual(testPlayer.xPos,500 + testPlayer.player_speed, "movement not working")

    """def run_after_play_button():
        sys.path.append(os.path.abspath("./src"))
        from .entity import *
        from view.imag import imag
        from .game_interface import Movement
        from pygame.locals import (
            K_LEFT,
            K_RIGHT,
            K_ESCAPE,
            KEYDOWN,
            K_SPACE,
            QUIT,
        )
        # Initialize pygame
        pygame.init()

        player = Player(64,64,1000,1000)
        screen = imag(1000,1000,player.getWidth(), player.getHeight())
        # Create the screen
        clock = pygame.time.Clock()
        running = True

        # Main loop
        while running:
            the game run while state of running is true,
            game can be stopped if user Quit using the exit buttom or exit through the Escape key
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
            """

