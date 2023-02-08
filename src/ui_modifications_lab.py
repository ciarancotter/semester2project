import pygame
from view.gameui import uielements, healthbar
from model.aiutilities import aiutilities

# Initialize pygame and create a window
pygame.init()
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    QUIT,
)

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
        image_to_load = pygame.image.load("src/view/assets/playerSprite.png")
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


dimensionX = 1280
dimensionY = 768

aiutilities.configure_openai()
legend = aiutilities.generate_monolith("tragic", "roman")

# get info about the screen we are using
infoobject = pygame.display.Info()

# Create the screen
screen = pygame.display.set_mode((dimensionX, dimensionY), pygame.HWSURFACE | pygame.DOUBLEBUF, 32)

# Created some UI elements.
myGamePanel = uielements.Panel(screen, 768, 768, 0, 0, "black")
myGamePanel.draw()

myUIPanel = uielements.Panel(screen, 512, 768, 768, 0, "orange")
myUIPanel.draw()

myTextBox = uielements.TextBox(screen, 25, 25, "monospace", 12, myUIPanel)
myTextBox.draw("Monke")

myHealthBar = healthbar.HealthBar(screen, myGamePanel, 100)
myHealthBar.drawMaxHealth()
myHealthBar.drawCurrentHealth()

pygame.display.update()

# Main game loop
running = True
spacePressed = False
currentLine = 0

player = Player()
clock = pygame.time.Clock()

pygame.display.set_caption("Boole Raider")

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
            
            elif event.key == pygame.K_SPACE and spacePressed == False:
                if currentLine < len(legend): 
                  myTextBox.erase()
                  myTextBox.draw(legend[currentLine])

                  spacePressed = True
                  currentLine += 1

                  myHealthBar.reduceHealth(10)
                  myHealthBar.drawCurrentHealth()
                
                else:
                  myTextBox.erase()
                  myTextBox.draw("End.")
                  break

        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                spacePressed = False
        
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    myGamePanel.erase("black")
    screen.blit(player.image, player.rect)
    # Get the set of keys pressed and check for user input
    pygame.display.update()

    # Update the display
    pygame.display.flip()

# Exit pygame
pygame.quit()
