import pygame

from pygame.locals import (
K_SPACE )


# initialize pygame
pygame.init()


# set screen size
screen = pygame.display.set_mode((800, 600))

# load the sprite sheet
sprite_sheet = pygame.image.load("src/view/assets/playerSprite.png")

# get individual sprites from the sprite sheet
character_width = 64
character_height = 64
columns = 3
rows = 2
character_sprites = [pygame.Surface((character_width, character_height)) for i in range(columns * rows)]

for i in range(rows):
    for j in range(columns):
        character_sprites[i * columns + j].blit(sprite_sheet, (0, 0), (j * character_width, i * character_height, character_width, character_height))

# set the starting position of the character on the screen
x = 100
y = 100

# set the starting sprite for the character
current_sprite_index = 0

# define a variable to keep track of the direction of the character
direction = "left"

counter = 0

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # get the keys that are pressed
    keys = pygame.key.get_pressed()

    # move the character to the right if the right key is pressed
    if keys[pygame.K_RIGHT]:
        x += 0.5
        direction = "right"
        current_sprite_index = 2
        counter +=1
        current_sprite_index = 1 + counter // 10 % 2
        
        
    # move the character to the left if the left key is pressed
    if keys[pygame.K_LEFT]:
        x -= 0.5
        direction = "left"

    # update the current sprite based on the direction of the character
    current_sprite_index = 0
    if direction == "left":
        counter +=2
        current_sprite_index = 1 + counter // 10 % 1
        current_sprite_index = (current_sprite_index + columns) % len(character_sprites)
        
    if direction == "right":
        counter +=2
        current_sprite_index = 1 + counter // 10 % 1

    # draw the current sprite of the character on the screen
    screen.blit(character_sprites[current_sprite_index], (x, y))

    # update the screen
    pygame.display.update()

# quit pygame
pygame.quit()
