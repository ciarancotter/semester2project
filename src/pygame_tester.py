###note need to fix the speed and gravity
import pygame

from pygame.locals import (
    #K_UP,
    #K_DOWN,  #probably won't need 
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    QUIT,
)

# Define constants for the screen width and height (this is just for now)
SCREEN_WIDTH = 768
SCREEN_HEIGHT = 768


#main character class
class Player(pygame.sprite.Sprite):
    """
        The Player Class is used to initilize the player and it's movements
        Attributes:
        - playerWidth: width of player image
        - playerHeight: hight of player image
        - playerxChange:  the x axes change for the player
        - playeryChange: the y axes change for the player
        - playerX: position of player in x axis
        - playerY: position of player in  y axis
        - playerImage: image of player
        Methods:
        - update(pressed_keys):  get the pressed key event and it apply it by moving right,left,jump or no action required 
    """
    def __init__(self):
        self.obj_ground= 0 #where player y is on the ground
        self.playerwidth = 50
        self.playerHeight = 75
        self.playerX = SCREEN_WIDTH / 2  #x co-ords for start position
        self.playerY = SCREEN_HEIGHT / 2  #y co-ords for start position
        image_to_load = pygame.image.load("src/view/assets/pharaoh_right_stand.png")
        self.image = pygame.Surface([self.playerwidth, self.playerHeight])
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.playerX
        self.rect.y = self.playerY
        self.facing = "down"
        self.player_speed = 2

    def update(self, pressed_keys):
        self.movement(pressed_keys)

        # self.rect.x += self.playerxChange
        # self.playerxChange = self.playerxChange *0.001
        # self.rect.y += self.playeryChange
        # self.playeryChange = self.playeryChange *0.001

        # # self.playerxChange = 0
        # # self.playeryChange = 0

        #collision_with_obj(player, box1)

    def movement(self, pressed_keys):
        #print(self.rect.y)
        self.obj_ground= SCREEN_HEIGHT+1
        #print(self.obj_ground, "ground")

        if pressed_keys[K_LEFT]  and self.rect.x >= 0 :

            self.rect.x -= self.player_speed
            self.facing = "left"

        if pressed_keys[K_RIGHT] and self.rect.x < SCREEN_WIDTH - self.playerwidth :
            self.rect.x += self.player_speed
            self.facing = "right"

        #jump again on;y if space is pressed and the charc y + it's hight is == to the screen hight +1(not sure why it's taking 1 extra out of the 
        # screen with the self.rect.y +self.playerHeight)
        if pressed_keys[K_SPACE] and self.rect.y +self.playerHeight == self.obj_ground :
            self.rect.y -= self.player_speed*20

        #maybe another if for jumping but for objects ?


        if self.rect.y <= SCREEN_HEIGHT - self.playerHeight :
           self.rect.y += self.player_speed




class Box(pygame.sprite.Sprite):

    def __init__(self):
        super(Box, self).__init__()
        self.boxWidth = 75
        self.boxHeight = 50
        self.boxX = 768-self.boxWidth
        self.boxY = 768 - self.boxHeight
        self.image = pygame.Surface([self.boxWidth, self.boxHeight])
        self.image.fill((194,178,128))
        self.rect = self.image.get_rect()
        self.rect.x = self.boxX
        self.rect.y = self.boxY



# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Keep main loop running
running = True
player = Player()
box1 = Box()
clock = pygame.time.Clock()

# Main loop
while running:
    """
    the game run while state of running is true,
    game can be stopped if user Quit using the exit buttom or exit through the Escape key
    """
    clock.tick(60)

    #player.gravity()
    for event in pygame.event.get():
        # Check if key pressed (KEYDOWN event)
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
   
        
        
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    screen.fill((0,0,0))
    screen.blit(player.image, player.rect)
    #pygame.draw.rect(screen, (255,0,0), (player.playerX, player.playerY, player.playerwidth, player.playerHeight))
    screen.blit(box1.image, box1.rect)
    # Get the set of keys pressed and check for user input
    pygame.display.update()


    # Update the display
    pygame.display.flip()
