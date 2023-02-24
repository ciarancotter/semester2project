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
    #print("kinect connected")
except ImportError:
    KINECT = False


# key controls
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_a,
    K_s,
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
    gamemanager.create_level_from_json()

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

        keys_pressed = pygame.key.get_pressed()
        movements_for_model = []

        # player movement
        if KINECT:
            if movementPoolMisc["turnleft"]:
                movements_for_model.append(Movement.left)
            elif movementPoolMisc["turnright"]:
                movements_for_model.append(Movement.right)
            elif movementPoolRead["jump"]:
                movements_for_model.append(Movement.jump)
            elif movementPoolRead["leftpunch"]:
                movements_for_model.append(Movement.left_punch)
            elif movementPoolRead["rightpunch"]:
                movements_for_model.append(Movement.right_punch)
            else:
                movements_for_model.append(Movement.no_movement)

        else:
            if keys_pressed[K_LEFT]:
                movements_for_model.append(Movement.left)
            elif keys_pressed[K_RIGHT]:
                movements_for_model.append(Movement.right)
            elif keys_pressed[K_UP]:
                movements_for_model.append(Movement.jump)
            elif keys_pressed[K_a]:
                movements_for_model.append(Movement.left_punch)
            elif keys_pressed[K_s]:
                movements_for_model.append(Movement.right_punch)
            else:
                movements_for_model.append(Movement.no_movement)

        # <-- Update calls go here -->
        gamemanager.update_model(movements_for_model)

        # loading the game panel for main menu and game
        gamepanel.checking_hover(pygame.mouse.get_pos())
        gamepanel.updateScene()


        # <-- View calls go here -->
        # game screen needs to be drawn after update call
        

        # refresh entire screen
        pygame.display.flip()
        #print(round(clock.get_fps(), 2))

    # Exit pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
