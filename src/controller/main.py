import pygame
import sys
import os

sys.path.append(os.path.abspath("./src"))
from model.gameobjects.game_interface import PlatformerGame
from view.gameui.scene import Scene


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
    pygame.init()

    # a boolean to ensure the game is running
    running = True

    clock = pygame.time.Clock()

    gamemanager = PlatformerGame()
    gamepanel = Scene(gamemanager)

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

        # loading the game panel for main menu and game
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
