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
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024

def collision_with_obj(object1, object2):
    collision_tolerance = 10
    if object1.rect.colliderect(object2):
        if abs(object2.rect.top - object1.rect.bottom) < collision_tolerance:
                object1.rect.bottom = object2.rect.top
        if abs(object2.rect.left - object1.rect.right) < collision_tolerance:
                object1.rect.right = object2.rect.left
        if abs(object2.rect.right - object1.rect.left) < collision_tolerance:
                object1.rect.left = object2.rect.right 


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
        #self.animationList = []
        #self.animationStep = 4
        #self.neg = 0
        self.playerwidth = 50
        self.playerHeight = 75
        #self.playerframeL = False
        #self.playerframeR = False
        self.playerxChange = 0
        self.playeryChange = 0
        # self.vel= 5 #velosity, how fast char move 
        self.playerX = SCREEN_WIDTH / 2  #x co-ords for start position
        self.playerY = SCREEN_HEIGHT / 2  #y co-ords for start position

        image_to_load = pygame.image.load("view/assets/pharaoh_right_stand.png")
        #self.playerImage = "frame.png"
        self.image = pygame.Surface([self.playerwidth, self.playerHeight])
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.playerX
        self.rect.y = self.playerY
        self.facing = "down"
        self.player_speed = 2

    def update(self, pressed_keys):
        self.movement(pressed_keys)

        self.rect.x += self.playerxChange
        self.playerxChange = self.playerxChange *0.001
        self.rect.y += self.playeryChange
        self.playeryChange = self.playeryChange *0.001

        self.playerxChange = 0
        self.playeryChange = 0

        collision_with_obj(player, box1)


    def movement(self, pressed_keys):
        if pressed_keys[K_LEFT]  and self.rect.x> 0:
            self.playerxChange -= self.player_speed
            self.facing = "left"

        if pressed_keys[K_RIGHT] and self.rect.x < SCREEN_WIDTH - self.playerwidth :
            self.playerxChange += self.player_speed
            self.facing = "right"

        if pressed_keys[K_SPACE] and self.rect.y  > 0 :
            self.playeryChange -= self.player_speed

        if self.rect.y < SCREEN_HEIGHT - self.playerHeight :
           self.rect.y += 1


    '''
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        """
        it get called when user press any keys of the 3 specified, Left Arrow, Right Arrow and Space 
        """
        #for vector movement x
        self.playerX = self.playerX + self.playerxChange
        self.playerxChange = self.playerxChange *0.10
        #for vector movement y
        self.playerY = self.playerY + self.playeryChange
        self.playeryChange = self.playeryChange *0.10

        if pressed_keys[K_LEFT] and self.playerX> 0:
            self.playerxChange = self.playerxChange - 0.2
            self.facing = "left"
            #self.playerX -= self.vel
        if pressed_keys[K_RIGHT] and self.playerX < SCREEN_WIDTH - self.playerwidth :
            self.playerxChange = self.playerxChange + 0.2
            self.facing = "right"

        if pressed_keys[K_SPACE] and self.playerY  > 0 :
            self.playeryChange = self.playeryChange - 4
            #self.playerY -= self.vel

        if self.playerY < SCREEN_HEIGHT - self.playerHeight :
            self.playerY += 2

        #collision_with_obj(player.rect, box1)
    '''
class Box(pygame.sprite.Sprite):

    def __init__(self):
        super(Box, self).__init__()
        self.boxWidth = 75
        self.boxHeight = 50
        self.boxX = 200
        self.boxY = 555  
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
# Main loop
while running:
    """
    the game run while state of running is true,
    game can be stopped if user Quit using the exit buttom or exit through the Escape key
    """
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
