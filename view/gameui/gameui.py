import pygame


class UITextBox:

    def __init__(self, screen, margin, font, fontsize):
        self.screen = screen
        self.margin = margin
        self.font = font
        self.fontsize = fontsize

    def draw(self, text: str):
        dimensions = self.screen.get_size()[0]
        box = pygame.Surface((dimensions - self.margin, dimensions // 8))
        box.fill("white")
        font = pygame.font.SysFont(self.font, self.fontsize)

        text = font.render(text, True, (0, 0, 0))
        text_rect = text.get_rect(center=(dimensions / 2, dimensions / 1.25))
        self.screen.blit(box, (self.margin // 2, dimensions * 0.75))
        self.screen.blit(text, text_rect)

    def erase(self):
        dimensions = self.screen.get_size()[0]
        box = pygame.Surface((dimensions - self.margin, dimensions // 8))
        box.fill("white")
        self.screen.blit(box, (self.margin // 2, dimensions * 0.75))
