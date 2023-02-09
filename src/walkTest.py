import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load("src/view/assets/menuBG.png") #test background

# load the sprite sheet
sprite_sheet = pygame.image.load("src/view/assets/playerSprite.png")

character_width = 64
character_height = 64
columns = 3
rows = 2
character_sprites = [pygame.Surface((character_width, character_height)) for i in range(columns * rows)]

for i in range(rows):
    for j in range(columns):
        # alpha channel to make background transparent
        transparent_sprite = pygame.Surface((character_width, character_height), pygame.SRCALPHA)
        # sprites copied onto tranparent background using blit
        transparent_sprite.blit(sprite_sheet, (0, 0), (j * character_width, i * character_height, character_width, character_height))
        # set to transparent colour
        transparent_sprite.set_colorkey((0, 0, 0, 0))
        # store in list
        character_sprites[i * columns + j] = transparent_sprite

x = 100
y = 100

# set the starting sprite for the character
current_sprite_index = 0

# define a variable to keep track of the direction of the character
direction = "left"

# set the delay between each frame
frame_delay = 10
frame_count = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))

    # get the keys that are pressed
    keys = pygame.key.get_pressed()

    # move the character to the right if the right key is pressed
    if keys[pygame.K_RIGHT]:
        x += 1
        direction = "right"
        frame_count += 1
        if frame_count == frame_delay:
            current_sprite_index = (current_sprite_index + 1) % columns
            frame_count = 0
    
      # move the character to the left if the left key is pressed
    if keys[pygame.K_LEFT]:
        x -= 1
        direction = "left"
        frame_count += 1
        if frame_count == frame_delay:
            current_sprite_index = columns + (current_sprite_index + 2) % columns
            frame_count = 0

    # update the current sprite based on the direction of the character
    if direction == "right":
        if current_sprite_index < columns:
            screen.blit(character_sprites[current_sprite_index], (x, y))
    else:
        if current_sprite_index >= columns:
            screen.blit(character_sprites[current_sprite_index], (x, y))

    pygame.display.update()

pygame.quit()
