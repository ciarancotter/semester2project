import pygame
import sys 
import os



class imag(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, playerwidth, playerHeight): 
    # Define constants for the screen width and height (this is just for now)
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.playerwidth = playerwidth
        self.playerHeight = playerHeight
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        image_to_load = pygame.image.load("src/view/assets/playerSprite.png")
        self.image = pygame.Surface([self.playerwidth, self.playerHeight])
        self.rect = self.image.get_rect()
        self.image.blit(image_to_load, self.rect)

        self.rect.x = 0
        self.rect.y = 0


    def create_screen(self):
        # Create the screen
        self.screen.fill((0,0,0))
        self.screen.blit(self.image, self.rect)
        pygame.display.update()
        pygame.display.flip()


    def update_xy(self, player):
        self.rect.x = player.xPos

        self.rect.y = player.yPos
