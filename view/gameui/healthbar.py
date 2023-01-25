"""A UI health indicator to inform the player of their remaining health.
"""

import pygame


class HealthBar:
    
    def __init__(self, maxHealth: int):
        self.maxHealth = maxHealth
        self.currentHealth = maxHealth

    def reduceHealth(self, damage: int):
        self.currentHealth -= damage

    def drawMaxHealth(self, screen):
        dimensions = screen.get_size()[0]
        bar = pygame.Surface((dimensions - (dimensions // 1.5), dimensions // 25))
        bar.fill("white")
        screen.blit(bar, (dimensions // 35, dimensions // 20))
        
    def drawCurrentHealth(self, screen, currentHealth):
        self.drawMaxHealth(screen)
        dimensions = screen.get_size()[0]
        dimensionX = (dimensions - (dimensions // 1.5)) * (currentHealth / self.maxHealth)
        bar = pygame.Surface((dimensionX, (dimensions // 25)))
        bar.fill("green")
        screen.blit(bar, (dimensions // 35, dimensions // 20))


