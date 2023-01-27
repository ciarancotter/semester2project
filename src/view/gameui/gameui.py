"""A utility to create a text box at the bottom of the screen.

This class can be used to create a text box with custom text in the Pygame UI.

Usage:

    myTextBox = UITextBox(screen, 20, "monospace", 14)
    myTextBox.draw("Pyramids look funny.")
    myTextBox.erase()
"""

import pygame


class UITextBox:
    """A UI text box to write a piece of dialogue or information at the bottom of the screen.

    A UI text box that scales quite well.

    Attributes:
        screen: The pygame screen.
        margin: The space between the window and the box at either side of it.
        font: The font used in the text box.
        fontsize: The size of the text.
    """

    def __init__(self, screen, margin, font, fontsize):
        """Inits UITextBox
        """
        self.screen = screen
        self.margin = margin
        self.font = font
        self.fontsize = fontsize

    def draw(self, text: str):
        """Draws the box to the screen.
        
        Args:
            text: The text to write in the box.
        """
        dimensions = self.screen.get_size()[0]
        box = pygame.Surface((dimensions - self.margin, dimensions // 8))
        box.fill("white")
        font = pygame.font.SysFont(self.font, self.fontsize)

        text = font.render(text, True, (0, 0, 0))
        text_rect = text.get_rect(center=(dimensions / 2, dimensions / 1.25))
        self.screen.blit(box, (self.margin // 2, dimensions * 0.75))
        self.screen.blit(text, text_rect)

    def erase(self):
        """Removes the current text.
        """
        dimensions = self.screen.get_size()[0]
        box = pygame.Surface((dimensions - self.margin, dimensions // 8))
        box.fill("white")
        self.screen.blit(box, (self.margin // 2, dimensions * 0.75))
