import pygame
import sys
import os

sys.path.append(os.path.abspath("./src"))
from model.gameobjects.game_interface import PlatformerGame
from view.gameui.scene import Scene

from model.gameobjects.public_enums import Movement


# key controls
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    QUIT,
)


def main() -> None:
    # Initialize pygame
    pygame.init()

    # a boolean to ensure the game is running
    running = True
    game_ran = False

    clock = pygame.time.Clock()

    gamemanager = PlatformerGame()
    gamepanel = Scene(gamemanager)
    gamepanel.initialiseMenuScene()

    # Main game loop
    while running:
        clock.tick(60)
        # exit the game in emergency
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:  # If user clicked close
                    running = False
                case pygame.KEYDOWN:  # If user hit the q key
                    match event.key:
                        case pygame.K_q:
                            running = False
                case pygame.MOUSEBUTTONUP:
                    gamepanel.check_play_pressed(event)


        # player movement 
        keys_pressed = pygame.key.get_pressed()
        
        if keys_pressed[K_LEFT]:
            gamemanager.update_model(Movement.left)
            print("left")
        if keys_pressed[K_RIGHT]:
            gamemanager.update_model(Movement.right)
            print("right")
        if keys_pressed[K_SPACE]:
            gamemanager.update_model(Movement.jump)
            print("jump")
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
