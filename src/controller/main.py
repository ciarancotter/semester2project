import pygame
import sys
import os
sys.path.append(os.path.abspath("../"))
from view.gameui.gameui import GameWindow#, ElementWindow

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
    myGameWindow.draw()

    # puts the text part of the display in
    """myElementWindow = ElementWindow(screen)
    myElementWindow.draw(myGameWindow)"""

    # puts the kinect part of the display in
    """myKineectWindow = ElementWindow(screen)
    myKinectWindow.draw(myGameWindow)"""

    #refresh entire screen
    pygame.display.flip()

    # a boolien to ensure the gmae is running 
    running = True

    # Main gmae loop 
    while running:
        # exit the gmae in emergency
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If user clicked close
                    running = False
            if event.type == pygame.KEYDOWN: # If user hit the q key
                if event.key == pygame.K_q:
                    running = False

        #<-- Update calls go here -->


        #<-- View calls go here -->


        #refresh entire screen
        pygame.display.flip()

    # Exit pygame
    pygame.quit()



if __name__ == "__main__":
    main()