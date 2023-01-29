import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,  #probably won't need 
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    QUIT,
)

# Define constants for the screen width and height (this is just for now)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


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
        self.animationList = []
        self.animationStep = 4
        #self.neg = 0
        self.playerwidth = 50
        self.playerHeight = 75
        self.playerframeL = False
        self.playerframeR = False
        self.playerxChange = 0
        self.playeryChange = 0
        # self.vel= 5 #velosity, how fast char move 
        self.playerX = SCREEN_WIDTH / 2  #x co-ords for start position
        self.playerY = SCREEN_HEIGHT / 2  #y co-ords for start position

        self.playerImage = "frame.png"


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
            #self.playerX -= self.vel
        if pressed_keys[K_RIGHT] and self.playerX < SCREEN_WIDTH - self.playerwidth :
            self.playerxChange = self.playerxChange + 0.2

        if pressed_keys[K_SPACE] and self.playerY  > 0 :
            self.playeryChange = self.playeryChange - 4
            #self.playerY -= self.vel

        if self.playerY < SCREEN_HEIGHT - self.playerHeight :
            self.playerY += 2
  




# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Keep main loop running
running = True
player = Player()
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
    pygame.draw.rect(screen, (255,0,0), (player.playerX, player.playerY, player.playerwidth, player.playerHeight))
    # Get the set of keys pressed and check for user input
    pygame.display.update()




    # Update the display
    pygame.display.flip()
