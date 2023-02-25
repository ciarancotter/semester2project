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
    print("kinect connected")
except ImportError:
    KINECT = False


# key controls
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_a,
    K_s,
    K_SPACE,
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
                gamepanel.check_play_pressed(event.pos)
                gamepanel.check_about_pressed(event.pos)

        keys_pressed = pygame.key.get_pressed()
        movements_for_model = []

        # player movement
        if KINECT:
            if movementPoolMisc["turnleft"]:
                movements_for_model.append(Movement.left)
            if movementPoolMisc["turnright"]:
                movements_for_model.append(Movement.right)
            if movementPoolRead["jump"]:
                movements_for_model.append(Movement.jump)
            if movementPoolRead["leftpunch"]:
                movements_for_model.append(Movement.left_punch)
            if movementPoolRead["rightpunch"]:
                movements_for_model.append(Movement.right_punch)
            if movements_for_model == []:
                movements_for_model = [Movement.no_movement]

        else:
            if keys_pressed[K_LEFT]:
                movements_for_model.append(Movement.left)
            if keys_pressed[K_RIGHT]:
                movements_for_model.append(Movement.right)
            if keys_pressed[K_UP] or keys_pressed[K_SPACE]:
                movements_for_model.append(Movement.jump)
            if keys_pressed[K_a]:
                movements_for_model.append(Movement.left_punch)
            if keys_pressed[K_s]:
                movements_for_model.append(Movement.right_punch)
            if movements_for_model == []:
                movements_for_model = [Movement.no_movement]

        # <-- Update calls go here -->
        gamemanager.update_model(movements_for_model)

        # loading the game panel for main menu and game
        pygame.mouse.set_visible(False)
        pygame.mouse.set_cursor(pygame.cursors.diamond)
        mouse_pos = pygame.mouse.get_pos()
        if KINECT:
            if movementPoolMisc["mousex"] > 0:
                if movementPoolMisc["mousey"] > 0:
                    mouse_pos = (int(movementPoolMisc["mousex"]), int(movementPoolMisc["mousey"]))
            if movementPoolRead["select"]:
                gamepanel.check_play_pressed(mouse_pos)
                gamepanel.check_about_pressed(mouse_pos)


        gamepanel.checking_hover(mouse_pos)
        gamepanel.updateScene()
        gamepanel.draw_pos(mouse_pos)
        gamepanel.draw_kinect()


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
