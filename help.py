import pygame
pygame.init()

WINDOW_SIZE = (1280, 780)
screen = pygame.display.set_mode(WINDOW_SIZE)

screen.fill((2,0,121))

black = (0, 0, 0)
white = (255, 255, 255)
gold = (255, 215, 0)

### load assets

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

walk_left_image = pygame.image.load("src/view/assets/help_sprite_walk_left.png")
walk_right_image = pygame.image.load("src/view/assets/help_sprite_walk_right.png")
punch_left_image =  pygame.image.load("src/view/assets/help_sprite_punch_left.png")
punch_right_image =  pygame.image.load("src/view/assets/help_sprite_punch_right.png")

walk_left_description = "To walk left"
walk_right_description = "To walk right"
punch_left_description = "To punch left"
punch_right_description = "To punch right"

enemy1 = pygame.image.load("src/view/assets/help_enemy_1.png")
enemy2 = pygame.image.load("src/view/assets/help_enemy_2.png")
enemy3 = pygame.image.load("src/view/assets/help_enemy_3.png")
enemy4 = pygame.image.load("src/view/assets/help_enemy_4.png")

# Load the spritesheet images and set the size of each sprite in the spritesheet
spritesheets = [
    (pygame.image.load("src/view/assets/help_screen/Bradley_twistleft_spritesheet.png"), 200, 300),
    (pygame.image.load("src/view/assets/help_screen/Patrick_twistright_spritesheet.png"), 200, 300),
    (pygame.image.load("src/view/assets/help_screen/Shaza_select_spritesheet.png"), 200, 300),
    (pygame.image.load("src/view/assets/help_screen/Niamh_punchleft_spritesheet.png"), 200, 300),
    (pygame.image.load("src/view/assets/help_screen/Sam_punchright_spritesheet.png"), 200, 300),
    (pygame.image.load("src/view/assets/help_screen/Ciaran_jump_spritesheet.png"), 200, 300)
]

# Define the rect object for each sprite in the spritesheets
sprite_rects = [
    [
        pygame.Rect((x, 0), (width, height)) for x in range(0, 800, width)
    ] for _, width, height in spritesheets
]

# Set the initial sprite index for each spritesheet to 0
sprite_indices = [0] * len(spritesheets)

# clock for frame rate
clock = pygame.time.Clock()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    ### ITEMS BOX

    square_position = (0, 50)
    square_size = (600, 200)
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

    font = pygame.font.SysFont("monospace", 20, bold=True)
    screen.blit(loot_image, (0, 120))
    loot_text = font.render(loot_description, True, (0,0,0))
    screen.blit(loot_text, (40, 190))

    screen.blit(jump_boost_image, (165, 120))
    jump_boost_text = font.render(jump_boost_description, True, (0,0,0))
    screen.blit(jump_boost_text, (170, 190))

    screen.blit(health_boost_image, (350, 120))
    health_boost_text = font.render(health_boost_description, True, (0,0,0))
    screen.blit(health_boost_text, (320, 190))

    screen.blit(invincibility_image, (500, 120))
    invincibility_text = font.render(invincibility_description, True, (0,0,0))
    screen.blit(invincibility_text, (500, 190))

    ### DOOR AND MONOLITH BOX

    square_position = (0, 300)
    square_size = (600, 228)
    border_radius = 20
    pygame.draw.rect(screen, (255, 215, 0), (square_position, square_size), border_radius=border_radius)

    border_position = (square_position[0] - 5, square_position[1] - 5)
    border_size = (square_size[0] + 10, square_size[1] + 10)
    border_radius = 20
    pygame.draw.rect(screen, (0, 0, 0), (border_position, border_size), 5, border_radius=border_radius)

    font = pygame.font.SysFont("monospace", 13, bold=True)

    screen.blit(monolith_image, (30, 320))
    monolith_text = font.render(monolith_description, True, (0,0,0))
    screen.blit(monolith_text, (140, 350))

    screen.blit(door_image, (0, 400))
    door_text = font.render(door_description, True, (0,0,0))
    screen.blit(door_text, (140, 450))

    ### ENEMIES BOX

    square_position = (0, 600)
    square_size = (600, 150)
    border_radius = 20
    pygame.draw.rect(screen, (255, 215, 0), (square_position, square_size), border_radius=border_radius)

    border_position = (square_position[0] - 5, square_position[1] - 5)
    border_size = (square_size[0] + 10, square_size[1] + 10)
    border_radius = 20
    pygame.draw.rect(screen, (0, 0, 0), (border_position, border_size), 5, border_radius=border_radius)

    font = pygame.font.SysFont("monospace", 30, bold=True)
    text = "DONT LET THEM GET TO YOU!"
    text_surface = font.render(text, True, black, gold)
    text_rect = text_surface.get_rect()
    text_rect.center = ((square_position[0] + square_size[0]) // 2, square_position[1] + 50)
    screen.blit(text_surface, text_rect)

    screen.blit(enemy1, (100, 670))
    screen.blit(enemy2, (200, 670))
    screen.blit(enemy3, (300, 670))
    screen.blit(enemy4, (400, 670))

    ### MOVEMENTS BOX

    square_position = (700, 0)
    square_size = (580, 780)
    
    pygame.draw.rect(screen, (255, 215, 0), (square_position, square_size))

    border_position = (square_position[0] - 5, square_position[1] - 5)
    border_size = (square_size[0] + 10, square_size[1] + 10)
    
    pygame.draw.rect(screen, (0, 0, 0), (border_position, border_size), 5)

    font = pygame.font.SysFont("monospace", 40, bold=True)
    text = "MOVEMENTS"
    text_surface = font.render(text, True, black, gold)
    text_rect = text_surface.get_rect()
    text_rect.center = (square_position[0] + square_size[0] // 2, square_position[1] + 50)
    screen.blit(text_surface, text_rect)

    #position of each row of spritesheets
    rows = [
        (700, 75), 
        (700, 430),
    ]
    
    # iterate through the spritesheets list and keep track of the index of each one
    for i, (spritesheet, width, height) in enumerate(spritesheets):
        sprite_index = sprite_indices[i]
        sprite_rect = sprite_rects[i][sprite_index]
        sprite = spritesheet.subsurface(sprite_rect)
        row_x, row_y = rows[i // 3]
        sprite_x = row_x + (i % 3) * 200
        sprite_y = row_y
        screen.blit(sprite, (sprite_x, sprite_y))
        sprite_indices[i] = (sprite_index + 1) % len(sprite_rects[i])

    font = pygame.font.SysFont("monospace", 15, bold=True)

    screen.blit(walk_left_image, (700, 350))
    walk_left_text = font.render(walk_left_description, True, (0,0,0))
    screen.blit(walk_left_text, (740, 410))

    screen.blit(walk_right_image, (910, 350))
    walk_right_text = font.render(walk_right_description, True, (0,0,0))
    screen.blit(walk_right_text, (940, 410))
    
    screen.blit(punch_right_image, (700, 720))
    punch_left_text = font.render(punch_left_description, True, (0,0,0))
    screen.blit(punch_left_text, (760, 750))

    screen.blit(punch_left_image, (910, 720))
    punch_left_text = font.render(punch_right_description, True, (0,0,0))
    screen.blit(punch_left_text, (960, 750))

    select_text = font.render("Select", True, (0,0,0))
    screen.blit(select_text, (1160, 410))

    jump_text = font.render("Jump", True, (0,0,0))
    screen.blit(jump_text, (1170, 750))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(6)

pygame.quit()
