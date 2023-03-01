import pygame
pygame.init()

WINDOW_SIZE = (1280, 780)
screen = pygame.display.set_mode(WINDOW_SIZE)

background_image = pygame.image.load("src/view/assets/aboutBG.png")

black = (0, 0, 0)
white = (255, 255, 255)
gold = (255, 215, 0)

logo = pygame.image.load("src/view/assets/logo.png")
logo = pygame.transform.scale(logo, (800, 150))

loot_image = pygame.image.load("src/view/assets/loot.png")
jump_boost_image = pygame.image.load("src/view/assets/jump_boost.png")
health_boost_image = pygame.image.load("src/view/assets/health_boost.png")

loot_description = "Loot"
jump_boost_description = "Jump Boost"
health_boost_description = "Health Boost"

font = pygame.font.Font(None, 30, bold=True)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_image, (0, 0))

    logo_x_pos = (WINDOW_SIZE[0] - logo.get_width()) // 2

    screen.blit(logo, (logo_x_pos, 20))

    # Draw a gold square with rounded corners under the developers
    square_position = (0, 190)
    square_size = (700, 400)
    border_radius = 20
    pygame.draw.rect(screen, (255, 215, 0), (square_position, square_size), border_radius=border_radius)

    # Draw a black border around the square
    border_position = (square_position[0] - 5, square_position[1] - 5)
    border_size = (square_size[0] + 10, square_size[1] + 10)
    border_radius = 20
    pygame.draw.rect(screen, (0, 0, 0), (border_position, border_size), 5, border_radius=border_radius)


    # title

    font = pygame.font.SysFont("monospace", 40, bold=True)
    text = "COLLECT YOUR ITEMS!"
    text_surface = font.render(text, True, (0,0,0), gold)
    text_rect = text_surface.get_rect()
    text_rect.center = ((square_position[0] + square_size[0]) // 2, square_position[1] + 50)
    screen.blit(text_surface, text_rect)

    # draw item images and descriptions
    font = pygame.font.SysFont("monospace", 24, bold=True)
    screen.blit(loot_image, (0, 300))
    loot_text = font.render(loot_description, True, (0,0,0))
    screen.blit(loot_text, (40, 400))

    screen.blit(jump_boost_image, (200, 300))
    jump_boost_text = font.render(jump_boost_description, True, (0,0,0))
    screen.blit(jump_boost_text, (200, 400))

    screen.blit(health_boost_image, (400, 300))
    health_boost_text = font.render(health_boost_description, True, (0,0,0))
    screen.blit(health_boost_text, (380, 400))

    pygame.display.flip()
    
pygame.quit()
