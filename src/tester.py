import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,  #probably won't need 
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height (this is just for now)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


#main character class
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()
        self.x = SCREEN_WIDTH / 2  #x co-ords for start position
        self.y = SCREEN_HEIGHT / 2  #y co-ords for start position
        #just for now its a black box
        self.surf = pygame.Surface((75, 50))
        self.surf.fill((0, 0, 0))
        #initial position
        self.rect = self.surf.get_rect(center=(self.x, self.y))

    def gravity(self):
        self.rect.move_ip(0, 1)

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        #might not be needed
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Instantiate player.(just black box rightnow )
player = Player()

# Keep main loop running
running = True

# Main loop
while running:
    player.gravity()

    for event in pygame.event.get():
        # Check if key pressed (KEYDOWN event)
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw the player on the screen
    screen.blit(player.surf, player.rect)

    # Update the display
    pygame.display.flip()
