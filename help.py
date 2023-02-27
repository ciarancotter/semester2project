import pygame
pygame.init()

WINDOW_SIZE = (1280, 780)
screen = pygame.display.set_mode(WINDOW_SIZE)

background_image = pygame.image.load("src/view/assets/aboutBG.png")

logo = pygame.image.load("src/view/assets/logo.png")
logo = pygame.transform.scale(logo, (800, 150))

loot_image = pygame.image.load("src/view/assets/loot.png")
jump_boost_image = pygame.image.load("src/view/assets/jump_boost.png")
health_boost_image = pygame.image.load("src/view/assets/health_boost.png")

loot_description = "Collect money for items"
jump_boost_description = "Higher jump"
health_boost_description = "Increase health"

font = pygame.font.Font(None, 30)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_image, (0, 0))

    logo_x_pos = (WINDOW_SIZE[0] - logo.get_width()) // 2

    screen.blit(logo, (logo_x_pos, 20))

    # draw item images and descriptions
    screen.blit(loot_image, (50, 200))
    screen.blit(jump_boost_image, (50, 350))
    screen.blit(health_boost_image, (50, 500))

    loot_text = font.render(loot_description, True, (255, 255, 255))
    screen.blit(loot_text, (150, 200))

    jump_boost_text = font.render(jump_boost_description, True, (255, 255, 255))
    screen.blit(jump_boost_text, (150, 350))

    health_boost_text = font.render(health_boost_description, True, (255, 255, 255))
    screen.blit(health_boost_text, (150, 500))

    pygame.display.flip()
    
pygame.quit()
