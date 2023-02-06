###note need to fix the speed and gravity
import pygame

from pygame.locals import (
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

def collision_with_obj(object1, object2):
    """
        Checks if object1 is colliding with object2: 

        object1 and object2 are passed into the function.
        They both must have the rect object(object1 is the player and object2 is the box/platform)
    """
    collision_tolerance = 10
    if object1.rect.colliderect(object2):
        if abs(object2.rect.top - object1.rect.bottom) < collision_tolerance:
                object1.rect.bottom = object2.rect.top
        if abs(object2.rect.left - object1.rect.right) < collision_tolerance:
                object1.rect.right = object2.rect.left
        if abs(object2.rect.right - object1.rect.left) < collision_tolerance:
                object1.rect.left = object2.rect.right 
        if abs(object1.rect.top - object2.rect.bottom) < collision_tolerance:
                object1.rect.top = object2.rect.bottom


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

        collision_with_obj(player, box1)
        collision_with_obj(player, box2)
        collision_with_obj(player, platform1)
        collision_with_obj(player, platform2)
        collision_with_obj(player, platform3)
        collision_with_obj(player, platform4)

    def movement(self, pressed_keys):
        #print(self.rect.y)
        #print(self.obj_ground, "before adding 1")

        #self.obj_ground= SCREEN_HEIGHT+1
        #print(self.obj_ground, "ground")

        if pressed_keys[K_LEFT]  and self.rect.x >= 0 :

            self.rect.x -= self.player_speed
            self.facing = "left"

        if pressed_keys[K_RIGHT] and self.rect.x < SCREEN_WIDTH - self.playerwidth :
            self.rect.x += self.player_speed
            self.facing = "right"

        #jump again on;y if space is pressed and the charc y + it's hight is == to the screen hight +1(not sure why it's taking 1 extra out of the 
        # screen with the self.rect.y +self.playerHeight)

        if pressed_keys[K_SPACE] and self.rect.y +self.playerHeight == SCREEN_HEIGHT :
            self.rect.y -= self.player_speed*20

        #maybe another if for jumping but for objects ?
        if self.rect.y < SCREEN_HEIGHT - self.playerHeight :
           self.rect.y += self.player_speed

        




class Box(pygame.sprite.Sprite):
    """
        The Box class is used to initilize the box and it's position:
        
        There's 3 arguments passed to it:
        -boxX: the x co-ordinate of the box
        -boxY: the y co-ordinate of the box
        -width: the width of the box
        -height: the height of the box
        
        Variables:
        -image: used to create the surface of the box using the boxWidth and boxHeight and it's a sandy colour.
        -rect: uses the pygame Rect object and the rect.x as x co-ordiantes and rect.y as y co-ordinates.
    """
    def __init__(self, boxX, boxY, width, height):
        super(Box, self).__init__()
        self.boxWidth = width
        self.boxHeight = height
        self.image = pygame.Surface([self.boxWidth, self.boxHeight])
        self.image.fill((194,178,128))
        self.rect = self.image.get_rect()
        self.rect.x = boxX
        self.rect.y = boxY



# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Keep main loop running
running = True
player = Player()

box_width = 75
box_height = 25

box1 = Box(500, SCREEN_HEIGHT-box_height, box_width, box_height)
box2 = Box(175, SCREEN_HEIGHT-box_height, box_width, box_height)

platform1 = Box(300, SCREEN_HEIGHT-100, box_width, box_height)
platform2 = Box(400, SCREEN_HEIGHT-150, box_width, box_height)
platform3 = Box(500, SCREEN_HEIGHT-200, box_width, box_height)
platform4 = Box(50, SCREEN_HEIGHT-100, box_width, box_height)

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
    #draw boxes and platforms
    screen.blit(box1.image, box1.rect)
    screen.blit(box2.image, box2.rect)
    screen.blit(platform1.image, platform1.rect)
    screen.blit(platform2.image, platform2.rect)
    screen.blit(platform3.image, platform3.rect)
    screen.blit(platform4.image, platform4.rect)
    # Get the set of keys pressed and check for user input
    pygame.display.update()


    # Update the display
    pygame.display.flip()
