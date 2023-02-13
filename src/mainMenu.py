import pygame
import sys

# Initialize pygame
pygame.init()

# Set screen size and title
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Main Menu")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (104, 119, 225)

# Load background image
background = pygame.image.load("src/view/assets/menuBG.png")
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

# Define buttons
#self.renderer
play_button = font.render("PLAY", True, BLACK)
#self.rect
play_rect = play_button.get_rect()
#self.rect.center
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

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Check if play button is clicked
        #if event.type == pygame.MOUSEBUTTONUP and play_rect.collidepoint(event.pos):

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

    # Draw buttons
    screen.blit(play_button, play_rect)
    screen.blit(leaderboard_button, leaderboard_rect)
    screen.blit(help_button, help_rect)
    screen.blit(about_button, about_rect)

    pygame.display.update()

pygame.quit()
sys.exit()
