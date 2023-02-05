import pygame
import sys
import os
sys.path.append(os.path.abspath("../"))
from view.gameui.gameui import GameWindow#, ElementWindow

import pygame_tester

# just for the moment(not sure where controls)
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    QUIT,
)

# Define constants for the screen width and height (this is just for now)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 768

def main():
    # Initialize pygame
    pygame.init()

    # Create the window to display the game in
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF, 32)

    # puts the game part of the display in
    myGameWindow = GameWindow(screen)
    """myGameWindow.draw()"""

    # puts the text part of the display in
    """myElementWindow = ElementWindow(screen)
    myElementWindow.draw(myGameWindow)"""

    # puts the kinect part of the display in
    """myKineectWindow = ElementWindow(screen)
    myKinectWindow.draw(myGameWindow)"""

    #refresh entire screen
    pygame.display.flip()

    # a boolean to ensure the game is running 
    running = True

    #get the player class from pygame_tester
    mainPlayer = pygame_tester.Player()
    #get the box class from pygame_tester
    blueBox = pygame_tester.Box()

    clock = pygame.time.Clock()

    # Main gmae loop 
    while running:
        clock.tick(60)
        # exit the game in emergency
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If user clicked close
                    running = False
            if event.type == pygame.KEYDOWN: # If user hit the q key
                if event.key == pygame.K_q:
                    running = False

        #<-- Update calls go here -->
        pressed_keys = pygame.key.get_pressed()
        mainPlayer.update(pressed_keys)

        #<-- View calls go here -->
        #game screen needs to be drawn after update call
        myGameWindow.draw()
        screen.blit(mainPlayer.image, mainPlayer.rect)
        screen.blit(blueBox.image, blueBox.rect)

        #refresh entire screen
        pygame.display.flip()

    # Exit pygame
    pygame.quit()



if __name__ == "__main__":
    main()