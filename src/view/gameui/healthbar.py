"""A UI health indicator to inform the player of their remaining health.

This class can be used to add a health bar to the Pygame UI, with methods to increase and decrease health.

Usage:

    myHealthBar = HealthBar(screen, gamePanel, 100)
    myHealthBar.reduceHealth(20)
    myHealthBar.drawMaxHealth()
    myHealthBar.drawCurrentHealth()
"""

import pygame


class HealthBar:
    """A UI health indicator to inform the player of their remaining health.

    A health indicator with methods to track the current health.

    Attributes:
        maxHealth: The maximum health of the player.
        currentHealth: The player's current health.
    """

    def __init__(self, screen, panel, maxHealth: int):
        """Inits Healthbar
        """
        self.screen = screen
        self.panel = panel
        self._maxHealth = maxHealth
        self._currentHealth = maxHealth

    def getMaxHealth(self):
        """Getter method for the maxHealth property
        """
        return self._maxHealth

    def getCurrentHealth(self):
        """Getter method for the currentHealth property
        """
        return self._currentHealth

    def setCurrentHealth(self, newHealth: int):
        """Setter method for the currentHealth property
        """
        self._currentHealth = newHealth

    def reduceHealth(self, damage: int):
        """Reduces the player's current health.

        Args:
            damage: The amount of health to reduce the current health by.
        """
        self.setCurrentHealth(self.getCurrentHealth() - damage)

    def drawMaxHealth(self):
        """Draws the maximum health bar, in white, to the screen.

        This is the background section of the healthbar.

        Args:
            screen: The pygame screen.
        """
        panelWidth = self.panel.getWidth()
        panelHeight = self.panel.getHeight()
        bar = pygame.Surface(
            (panelWidth - (panelWidth // 1.5), panelWidth // 25))
        bar.fill("white")
        self.screen.blit(bar, (panelWidth // 35, panelWidth // 20))

    def drawCurrentHealth(self):
        """Draws the current health, in green, to the screen.
        
        This is the variable part of the healthbar.

        Args:
            screen: The pygame screen.
            panel: The panel to draw the health bar to.
            currentHealth: The current health amount, which must be less than maxHealth.
        """

        self.drawMaxHealth()
        panelWidth = self.panel.getWidth()
        barX = (panelWidth - (panelWidth // 1.5)) * (self.getCurrentHealth() /
                                                     self.getMaxHealth())
        bar = pygame.Surface((barX, (panelWidth // 25)))
        bar.fill("green")
        self.screen.blit(bar, (panelWidth // 35, panelWidth // 20))
