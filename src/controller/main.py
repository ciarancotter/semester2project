import pygame
import sys
import os

sys.path.append(os.path.abspath("./src"))
from model.gameobjects.game_interface import PlatformerGame
from view.gameui.scene import Scene

from model.gameobjects.public_enums import Movement

try:
    from pykinect2 import PyKinectV2
    from shared_memory_dict import SharedMemoryDict
    KINECT = True
except ImportError:
    KINECT = False


# key controls
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    K_UP,
    K_p,
    K_a,
    K_s,
    K_DOWN,
    QUIT,
)


def main() -> None:
    # Initialize pygame
    pygame.init()

    # a boolean to ensure the game is running
    running = True
    game_ran = False

    if KINECT:
        # init shared memeory pool
        movementPoolRead = SharedMemoryDict(name='movementPoolRead', size=1024)
        movementPoolMisc = SharedMemoryDict(name='movementPoolMisc', size=1024)
        # start python


    clock = pygame.time.Clock()

    gamemanager = PlatformerGame()
    gamepanel = Scene(gamemanager)
    gamepanel.initialiseMenuScene()

    # Main game loop
    while running:
        clock.tick(60)
        # exit the game in emergency
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If user clicked close
                    running = False
            if event.type == pygame.KEYDOWN: # If user hit the q key
                if event.key == pygame.K_q:
                    running = False
            #check if play button is clicked in the main menu
            if event.type == pygame.MOUSEBUTTONUP:
                gamepanel.check_play_pressed(event)


        # player movement
        if KINECT:
            if movementPoolMisc["turnleft"]:
                gamemanager.update_model(Movement.left)
            elif movementPoolMisc["turnright"]:
                gamemanager.update_model(Movement.right)
            elif movementPoolRead["jump"]:
                gamemanager.update_model(Movement.jump)
            elif movementPoolRead["leftpunch"]:
                gamemanager.update_model(Movement.left_punch)
            elif movementPoolRead["rightpunch"]:
                gamemanager.update_model(Movement.right_punch)
            else:
                gamemanager.update_model(Movement.no_movement)

        else:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[K_LEFT]:
                gamemanager.update_model(Movement.left)
            elif keys_pressed[K_RIGHT]:
                gamemanager.update_model(Movement.right)
            elif keys_pressed[K_UP]:
                gamemanager.update_model(Movement.jump)
            elif keys_pressed[K_a]:
                gamemanager.update_model(Movement.left_punch)
            elif keys_pressed[K_s]:
                gamemanager.update_model(Movement.right_punch)
            else:
                gamemanager.update_model(Movement.no_movement)

            

        # <-- Update calls go here -->


        # loading the game panel for main menu and game
        gamepanel.checking_hover(pygame.mouse.get_pos())
        gamepanel.updateScene()



        

        

        # <-- View calls go here -->
        # game screen needs to be drawn after update call
        

        # refresh entire screen
        pygame.display.flip()

    # Exit pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
