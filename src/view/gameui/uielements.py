"""A utility to create a UI elements in pygame.

This module can be used to create UI elements.

Usage:

    gamePanel = Panel(screen, 768, 768, 0, 0, "blue")
    gamePanel.draw()

    textBox = TextBox(screen, 20, 20, "monospace", 14, gamePanel)
    textBox.draw("Pyramids look funny.")
    textBox.erase()
"""

import pygame
from .scene import Scene

class TextBox:
    """A UI text box to write a piece of dialogue or information at the bottom of the screen.

    A UI text box that scales quite well.

    Attributes:
        screen: The pygame screen.
        marginX: The space between the window and the box at either side of it.
        marginY: The space above and below the box.
        font: The font used in the text box.
        fontsize: The size of the text.
        window: The panel to draw the box to.

    """

    def __init__(self, screen: pygame.screen, marginX: int, marginY: int, font: str,
                 fontsize: int, panel: Scene) -> None:
        """Inits UITextBox
        """
        self.screen = screen
        self.marginX = marginX
        self.marginY = marginY
        self.font = font
        self.fontsize = fontsize
        self.panel = panel

    def draw(self, text: str) -> None:
        """Draws the box to the screen.
        
        Args:
            text: The text to write in the box.
        """

        screen_width = 512
        screen_height = 768
        box_width = screen_width // 4
        box = pygame.Surface((box_width, screen_height))

        panel_width, panel_height = self.panel.getWidth(), self.panel.getHeight(
        )
        box_width, box_height = (panel_width -
                                 self.marginX), ((panel_height // 8) -
                                                 self.marginY)

        box = pygame.Surface((box_width, box_height))
        box_position = (self.panel.getX() + (self.marginX // 2),
                        (self.panel.getY() + (self.marginY // 2)))

        box.fill("white")
        font = pygame.font.SysFont(self.font, self.fontsize)

        text = font.render(text, True, (0, 0, 0))
        text_rect = text.get_rect(center=(box_position[0] + (box_width // 2),
                                          box_height // 2 +
                                          (self.marginY // 2)))

        self.screen.blit(box, box_position)
        self.screen.blit(text, text_rect)

    def erase(self) -> None:
        """Removes the current text.
        """
        panel_width, panel_height = self.panel.getWidth(), self.panel.getHeight(
        )
        box_width, box_height = (panel_width -
                                 self.marginX), ((panel_height // 8) -
                                                 self.marginY)
        box = pygame.Surface((box_width, box_height))
        box.fill("white")
        box_position = (self.panel.getX() + (self.marginX // 2),
                        (self.panel.getY() + (self.marginY // 2)))
        self.screen.blit(box, box_position)


class Panel:
    """A UI Panel to draw UI features (text boxes, buttons, etc) to.

    A customisable panel class to draw objects onto.

    Attributes:
        - screen: The screen to draw the panel onto.
        - width: The width of the panel.
        - height: The height of the panel.
        - x: The x-coordinate of the panel's upper-left corner.
        - y: The y-coordinate of the panel's upper-left corner.
    """

    def __init__(self, screen: pygame.screen, width: int, height: int, x: int, y: int,
                 colour: str) -> None:
        """Inits the Panel class
        """
        self.screen = screen
        self._width = width
        self._height = height
        self._x = x
        self._y = y

        self.panel = pygame.Surface((width, height))
        self.panel.fill(colour)

    def getWidth(self) -> int:
        """Getter method for the width property
        """
        return self._width

    def getHeight(self) -> int:
        """Getter method for the height property
        """
        return self._height

    def getX(self) -> int:
        """Getter method for the x property.
        """
        return self._x

    def getY(self) -> int:
        """Getter method for the y property.
        """
        return self._y

    def draw(self) -> None:
        """Method to draw the window to a screen.
        """
        self.screen.blit(self.panel, (self.getX(), self.getY()))

    def erase(self, colour: str) -> None:
        """Method to erase the panel.
        """
        self.panel.fill(colour)


class Button:

    def __init__(self, text: str, button_center: tuple) -> None:
        self.text = text
        self.font = pygame.font.Font(None, 85)
        self.renderer = self.font.render(self.text, True, "black")
        self.rect = self.renderer.get_rect()
        self.rect.center = button_center

    def setBlue(self) -> None:
        self.renderer = self.font.render(self.text, True, "blue")
