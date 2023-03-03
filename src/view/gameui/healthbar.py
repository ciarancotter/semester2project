"""A UI health indicator to inform the player of their remaining health.

This class can be used to add a health bar to the Pygame UI, with methods to increase and decrease health.

Usage:

    myHealthBar = HealthBar(screen, gamePanel, 100)
    myHealthBar.reduceHealth(20)
    myHealthBar.drawMaxHealth()
    myHealthBar.drawCurrentHealth()
"""

import pygame
from model.gameobjects.entity import Player


class HealthBar:
    """A UI health indicator to inform the player of their remaining health.

    A health indicator with methods to track the current health.

    Attributes:
        maxHealth: The maximum health of the player.
        currentHealth: The player's current health.
    """

    def __init__(self, screen, panel, player: Player) -> None:
        """Inits Healthbar
        """
        self.screen = screen
        self.panel = panel
        self.player = player


    def draw_health(self) -> None:
        """Draws the complete healthbar.
        """
 
        panel_width = self.panel.get_width()

        max_health_bar = pygame.Surface(
            (panel_width - (panel_width // 1.5), panel_width // 25))

        current_health_bar_x = (
                (panel_width - (panel_width // 1.5)) * 
                (self.player.health // self.player._max_health)
                )
        current_health_bar = pygame.Surface((current_health_bar_x, (panel_width // 25)))
        
        max_health_bar.fill("white")
        current_health_bar.fill("green")

        self.screen.blit(max_health_bar, (panel_width // 35, panel_width // 20))
        self.screen.blit(current_health_bar, (panel_width // 35, panel_width // 20))


class LevelIndicator:
    """The LevelIndicator indicates the current level to the player. 

        Attributes:
            - screen: The Pygame screen upon which the indicator is drawn.
            - panel: The UI panel object upon which the indicator is drawn.
    """

    def __init__(self, screen, panel):
        """Inits the LevelIndicator class.
        """
        self.screen = screen
        self.panel = panel
        self.font = "monospace"
        self.fontsize = 16

    def draw(self, level: int) -> None:
        """Draws the level to the screen.
            Attributes:
                level: The current level.
        """
         
        text = str(level)
        screen_width = 496
        screen_height = 784
        font = pygame.font.SysFont(self.font, self.fontsize)
        text_value = "Level " + text
        text_value = font.render(text_value, True, (0, 0, 0))
        text_rect = text_value.get_rect(center=(784 + self.panel.get_width() // 2, self.panel.get_height() // 4))
        self.screen.blit(text_value, text_rect)

