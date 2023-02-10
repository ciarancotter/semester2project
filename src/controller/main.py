import pygame
import sys
import os
sys.path.append(os.path.abspath("./src"))
#print(sys.path)
#from view.gameui.uielements import Panel

# Initialize pygame
pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

'''---------------------------'''
# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (104, 119, 225)

# Define font and size
font = pygame.font.Font(None, 85)

#------ Define buttons for main menu ---------
play_button = font.render("PLAY", True, BLACK)
play_rect = play_button.get_rect()
play_rect.center = (512, 330)

leaderboard_button = font.render("LEADERBOARD", True, BLACK)
leaderboard_rect = leaderboard_button.get_rect()
leaderboard_rect.center = (512, 430)

help_button = font.render("HELP", True, BLACK)
help_rect = help_button.get_rect()
help_rect.center = (512, 530)

about_button = font.render("ABOUT", True, BLACK)
about_rect = about_button.get_rect()
about_rect.center = (512, 630)
'''------------------------------'''

#function to open player panel 
def open_player_panel():
    from ui_modifications_lab import Player
    #GamePanel.draw()
    Player()

#key controls
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    QUIT,
)

def main():
    # Set screen size and title for main menu
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    '''---------------------'''
    pygame.display.set_caption("Main Menu")

    # Load background image for main menu
    background = pygame.image.load("./src/view/assets/menuBG.png")
    background = pygame.transform.scale(background, (1024, 768))

    logo = pygame.image.load("src/view/assets/logo.png")
    logo = pygame.transform.scale(logo, (800, 150))

    # Define font and size
    font = pygame.font.Font(None, 85)

    # Get the rectangle for the image
    logo_rect = logo.get_rect()

    # Set the position of the image on the screen
    logo_rect.center = (512, 150)

    # Draw background
    screen.blit(background, (0, 0))

    # Draw logo
    screen.blit(logo, logo_rect)

    '''-----------------------'''

    # load game panel for game
    #GamePanel = Panel(screen, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, BLACK)

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

    #get the player class from pygame_tester(needs to be changed)
    #mainPlayer = pygame_tester.Player()
    #get the box class from pygame_tester
    #blueBox = pygame_tester.Box()

    clock = pygame.time.Clock()

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
            '''----------------------------'''
            #check if play button is clicked in the main menu
            if event.type == pygame.MOUSEBUTTONUP and play_rect.collidepoint(event.pos):
                open_player_panel()

        mouse_pos = pygame.mouse.get_pos()

        if play_rect.collidepoint(mouse_pos):
            play_button = font.render("PLAY", True, BLUE)
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            play_button = font.render("PLAY", True, BLACK)
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

        # Check if mouse is hovering over buttons and effect
        if play_rect.collidepoint(mouse_pos):
            play_button = font.render("PLAY", True, BLUE)
        else:
            play_button = font.render("PLAY", True, BLACK)

        if leaderboard_rect.collidepoint(mouse_pos):
            leaderboard_button = font.render("LEADERBOARD", True, BLUE)
        else:
            leaderboard_button = font.render("LEADERBOARD", True, BLACK)

        if help_rect.collidepoint(mouse_pos):
            help_button = font.render("HELP", True, BLUE)
        else:
            help_button = font.render("HELP", True, BLACK)

        if about_rect.collidepoint(mouse_pos):
            about_button = font.render("ABOUT", True, BLUE)
        else:
            about_button = font.render("ABOUT", True, BLACK)

        # Draw buttons for main menu
        screen.blit(play_button, play_rect)
        screen.blit(leaderboard_button, leaderboard_rect)
        screen.blit(help_button, help_rect)
        screen.blit(about_button, about_rect)
        '''-----------------------------'''

        pygame.display.update()

        #<-- Update calls go here -->
        pressed_keys = pygame.key.get_pressed()
        #mainPlayer.update(pressed_keys)
        #pygame_tester.collision_with_obj(mainPlayer, blueBox)

        #<-- View calls go here -->
        #game screen needs to be drawn after update call
        #myGameWindow.draw()
        #GamePanel.draw()
        #screen.blit(mainPlayer.image, mainPlayer.rect)
        #screen.blit(blueBox.image, blueBox.rect)

        #refresh entire screen
        pygame.display.flip()

    # Exit pygame
    pygame.quit()
    #sys.exit()


if __name__ == "__main__":
    main()