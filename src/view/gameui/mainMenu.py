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
TRANSPARENT = (0, 0, 0, 0)

# Load background image
background = pygame.image.load("src/view/assets/menuBG.png")
background = pygame.transform.scale(background, (1024, 768))

# Define font and size
font = pygame.font.Font(None, 85)

# Define buttons
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

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Check if play button is clicked
        if event.type == pygame.MOUSEBUTTONUP and play_rect.collidepoint(event.pos):
            # Open Panel
            from uielements import Panel
            Panel()
    
    mouse_pos = pygame.mouse.get_pos()

    if play_rect.collidepoint(mouse_pos):
        play_button = font.render("PLAY", True, (104, 119, 225))
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
    else:
        play_button = font.render("PLAY", True, BLACK)
        pygame.mouse.set_cursor(*pygame.cursors.arrow)


    # Check if mouse is hovering over buttons and effect
    if play_rect.collidepoint(mouse_pos):
        play_button = font.render("PLAY", True, (104, 119, 225))
    else:
        play_button = font.render("PLAY", True, BLACK)

    if leaderboard_rect.collidepoint(mouse_pos):
        leaderboard_button = font.render("LEADERBOARD", True, (104, 119, 225))
    else:
        leaderboard_button = font.render("LEADERBOARD", True, BLACK)

    if help_rect.collidepoint(mouse_pos):
        help_button = font.render("HELP", True, (104, 119, 225))
    else:
        help_button = font.render("HELP", True, BLACK)

    if about_rect.collidepoint(mouse_pos):
        about_button = font.render("ABOUT", True, (104, 119, 225))
    else:
        about_button = font.render("ABOUT", True, BLACK)

    # Draw background
    screen.blit(background, (0, 0))

    # Draw buttons
    screen.blit(play_button, play_rect)
    screen.blit(leaderboard_button, leaderboard_rect)
    screen.blit(help_button, help_rect)
    screen.blit(about_button, about_rect)

    pygame.display.update()

pygame.quit()
sys.exit()
