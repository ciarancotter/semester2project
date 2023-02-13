import pygame
import sys
import os

sys.path.append(os.path.abspath("./src"))
#from model.gameobjects.game_interface import *
#from view.gameui.scene import *

# Initialize pygame
pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
'''---------------------------'''


# function to open player panel
def open_player_panel():
    from ui_modifications_lab import Player
    # GamePanel.draw()
    Player()


'''---------------------------'''

# key controls
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    QUIT,
)


def main():
    # Initialize pygame
    #pygame.init()

    # Set screen size and title for main menu
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # loading the game panel for main menu and game
    '''-----commented out until for the moment --------
    game = PlatformerGame()
    ctx = game.get_render_ctx()
    for block in ctx.blocks:
        print(block.coordinates)
    myScene = Scene(game)
    myScene.initialiseMenuScene()   #not sure if this should go in controller
    myScene.initialiseGameScene()   #not sure if this should go in controller
    myScene.updateScene()
    ----------------------'''

    # puts the text part of the display in
    """myElementWindow = ElementWindow(screen)
    myElementWindow.draw(myGameWindow)"""

    # puts the kinect part of the display in
    """myKineectWindow = ElementWindow(screen)
    myKinectWindow.draw(myGameWindow)"""

    # refresh entire screen
    pygame.display.flip()

    # a boolean to ensure the game is running
    running = True

    # get the player class from pygame_tester(needs to be changed)
    # mainPlayer = pygame_tester.Player()
    # get the box class from pygame_tester
    # blueBox = pygame_tester.Box()

    clock = pygame.time.Clock()

    # Main game loop
    while running:
        clock.tick(60)
        # exit the game in emergency
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If user clicked close
                running = False
            if event.type == pygame.KEYDOWN:  # If user hit the q key
                if event.key == pygame.K_q:
                    running = False

        # <-- Update calls go here -->
        pressed_keys = pygame.key.get_pressed()
        # mainPlayer.update(pressed_keys)
        # pygame_tester.collision_with_obj(mainPlayer, blueBox)

        # <-- View calls go here -->
        # game screen needs to be drawn after update call
        # myGameWindow.draw()
        # GamePanel.draw()
        # screen.blit(mainPlayer.image, mainPlayer.rect)
        # screen.blit(blueBox.image, blueBox.rect)

        # refresh entire screen
        pygame.display.flip()

    # Exit pygame
    pygame.quit()
    # sys.exit()


if __name__ == "__main__":
    main()
