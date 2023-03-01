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
invincibility_image = pygame.image.load("src/view/assets/invincibility.png")
monolith_image = pygame.image.load("src/view/assets/monolith.png")
door_image = pygame.image.load("src/view/assets/door.png")

loot_description = "Loot"
jump_boost_description = "Jump Boost"
health_boost_description = "Health Boost"
invincibility_description = "Shield"
monolith_description = "Stand by this monolith to continue the story."
door_description = "Get to the door and walk through to complete each level."

spritesheets = [
    ("src/view/assets/help_screen/Bradley_twistleft_spritesheet.png", 200, 300),
    ("src/view/assets/help_screen/Patrick_twistright_spritesheet.png", 200, 300),
    ("src/view/assets/help_screen/Shaza_select_spritesheet.png", 200, 300),
    ("src/view/assets/help_screen/Niamh_punchleft_spritesheet.png", 200, 300),
    ("src/view/assets/help_screen/Sam_punchright_spritesheet.png", 200, 300),
    ("src/view/assets/help_screen/Ciaran_jump_spritesheet.png", 200, 300),
]

sprite_rects = [
    [
        pygame.Rect((x, 0), (width, height)) for x in range(0, 800, width)
    ] for filename, width, height in spritesheets
]

# Set the initial sprite index for each spritesheet to 0
sprite_indices = [0] * len(spritesheets)

font = pygame.font.Font(None, 30, bold=True)

clock = pygame.time.Clock()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_image, (0, 0))

    logo_x_pos = (WINDOW_SIZE[0] - logo.get_width()) // 2

    screen.blit(logo, (logo_x_pos, 20))

    square_position = (0, 190)
    square_size = (700, 300)
    border_radius = 20
    pygame.draw.rect(screen, (255, 215, 0), (square_position, square_size), border_radius=border_radius)

    border_position = (square_position[0] - 5, square_position[1] - 5)
    border_size = (square_size[0] + 10, square_size[1] + 10)
    border_radius = 20
    pygame.draw.rect(screen, (0, 0, 0), (border_position, border_size), 5, border_radius=border_radius)

    font = pygame.font.SysFont("monospace", 40, bold=True)
    text = "COLLECT YOUR ITEMS!"
    text_surface = font.render(text, True, black, gold)
    text_rect = text_surface.get_rect()
    text_rect.center = ((square_position[0] + square_size[0]) // 2, square_position[1] + 50)
    screen.blit(text_surface, text_rect)

    font = pygame.font.SysFont("monospace", 24, bold=True)
    screen.blit(loot_image, (0, 300))
    loot_text = font.render(loot_description, True, (0,0,0))
    screen.blit(loot_text, (40, 400))

    screen.blit(jump_boost_image, (200, 300))
    jump_boost_text = font.render(jump_boost_description, True, (0,0,0))
    screen.blit(jump_boost_text, (195, 400))

    screen.blit(health_boost_image, (430, 300))
    health_boost_text = font.render(health_boost_description, True, (0,0,0))
    screen.blit(health_boost_text, (380, 400))

    screen.blit(invincibility_image, (600, 300))
    invincibility_text = font.render(invincibility_description, True, (0,0,0))
    screen.blit(invincibility_text, (600, 400))

    square_position = (0, 500)
    square_size = (700, 190)
    border_radius = 20
    pygame.draw.rect(screen, (255, 215, 0), (square_position, square_size), border_radius=border_radius)

    border_position = (square_position[0] - 5, square_position[1] - 5)
    border_size = (square_size[0] + 10, square_size[1] + 10)
    border_radius = 20
    pygame.draw.rect(screen, (0, 0, 0), (border_position, border_size), 5, border_radius=border_radius)

    font = pygame.font.SysFont("monospace", 17, bold=True)

    screen.blit(monolith_image, (40, 500))
    monolith_text = font.render(monolith_description, True, (0,0,0))
    screen.blit(monolith_text, (120, 530))

    screen.blit(door_image, (10, 562))
    door_text = font.render(door_description, True, (0,0,0))
    screen.blit(door_text, (140, 620))

    for i, (filename, _, _) in enumerate(spritesheets):
        current_sprite_rect = sprite_rects[i][sprite_indices[i]]
        spritesheet = pygame.image.load(filename)
        screen.blit(spritesheet, (i * 200, 0), current_sprite_rect)

        sprite_indices[i] = (sprite_indices[i] + 1) % len(sprite_rects[i])
    
    pygame.display.flip()
    clock.tick(6)
pygame.quit()
