"""A utility to create a text box at the bottom of the screen.

This class can be used to create a text box with custom text in the Pygame UI.

Usage:

    myTextBox = UITextBox(screen, 20, "monospace", 14)
    myTextBox.draw("Pyramids look funny.")
    myTextBox.erase()
"""

import pygame
import sys


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
        screen_width = 512
        screen_height = 768
        box_width = screen_width // 4
        box = pygame.Surface((box_width, screen_height))
        box.fill("white")
        font = pygame.font.SysFont(self.font, self.fontsize)

        text = font.render(text, True, (0, 0, 0))
        text_rect = text.get_rect(center=(3 * box_width // 2, screen_height // 2))
        self.screen.blit(box, (3 * screen_width // 4, 0))
        self.screen.blit(text, text_rect)

        #16x9 for camera (keep revalent for 1080p)


    def erase(self):
        """Removes the current text.
        """
        dimensions = self.screen.get_size()[0]
        box = pygame.Surface((dimensions - self.margin, dimensions // 8))
        box.fill("white")
        self.screen.blit(box, (self.margin // 2, dimensions * 0.75))


class GameWindow:
    def __init__(self, screen):
        self.miniWindow = pygame.Surface((768, 768))
        self.miniWindow.fill("orange")
        self.screen = screen
        self.dimensions = self.screen.get_size()

    def draw(self):
        self.screen.blit(self.miniWindow, (0, 0))

    def getMiniWindow(self):
        return self.miniWindow

class ElementWindow:
    def __init__(self, screen):
        self.elementWindow = pygame.Surface((512, 768))
        self.elementWindow.fill("green")
        self.screen = screen
        self.screenDimensions = self.screen.get_size()

    def draw(self, game: GameWindow):
        self.screen.blit(self.elementWindow, game.getMiniWindow().get_rect().topright)

pygame.init()
screen = pygame.display.set_mode((1024, 768))

game = GameWindow(screen)
element = ElementWindow(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    game.draw()
    element.draw(game)
    pygame.display.update()

