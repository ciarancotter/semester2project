"""A UI health indicator to inform the player of their remaining health.

This class can be used to add a health bar to the Pygame UI, with methods to increase and decrease health.

Usage:

    myHealthBar = HealthBar(100)
    myHealthBar.reduceHealth(20)
    myHealthBar.drawMaxHealth(screen)
    myHealthBar.drawCurrentHealth(screen)
"""

import pygame


class HealthBar:
    """A UI health indicator to inform the player of their remaining health.

    A health indicator with methods to track the current health.

    Attributes:
        maxHealth: The maximum health of the player.
        currentHealth: The player's current health.
    """

    def __init__(self, maxHealth: int):
        """Inits Healthbar
        """
        self.maxHealth = maxHealth
        self.currentHealth = maxHealth

    def reduceHealth(self, damage: int):
        """Reduces the player's current health.

        Args:
            damage: The amount of health to reduce the current health by.
        """
        self.currentHealth -= damage

    def drawMaxHealth(self, screen):
        """Draws the maximum health bar, in white, to the screen.

        This is the background section of the healthbar.

        Args:
            screen: The pygame screen.
        """
        dimensions = screen.get_size()[0]
        bar = pygame.Surface((dimensions - (dimensions // 1.5), dimensions // 25))
        bar.fill("white")
        screen.blit(bar, (dimensions // 35, dimensions // 20))
        
    def drawCurrentHealth(self, screen, currentHealth):
        """Draws the current health, in green, to the screen.
        
        This is the variable part of the healthbar.

        Args:
            screen: The pygame screen.
            currentHealth: The current health amount. This must be less than maxHealth.
        """

        self.drawMaxHealth(screen)
        dimensions = screen.get_size()[0]
        dimensionX = (dimensions - (dimensions // 1.5)) * (currentHealth / self.maxHealth)
        bar = pygame.Surface((dimensionX, (dimensions // 25)))
        bar.fill("green")
        screen.blit(bar, (dimensions // 35, dimensions // 20))


