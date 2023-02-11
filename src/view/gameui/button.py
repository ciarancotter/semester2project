import pygame

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (104, 119, 225)

class Button:
    # Define buttons
    play_button = font.render("PLAY", True, BLACK)
    play_rect = play_button.get_rect()
    play_rect.center = (512, 330)

    leaderboard_button = font.render("LEADERBOARD", True, BLACK)
    leaderboard_rect = leaderboard_button.get_rect()
    leaderboard_rect.center = (512, 430)

    help_button = font.render("HELP", True, BLACK)
    help_rect = help_button.get_rect()
    help_rect.center = (512, 530)

    about_button = font.render("ABOUT", True, BLACK)
    about_rect = about_button.get_rect()
    about_rect.center = (512, 630)

    def __init__(self, screen, text, position):
        self.screen = screen
        self.text = text
        #self.font = font
        self.button = self.font.render(text, True, BLACK)
        self.rect = self.button.get_rect()
        self.rect.center = position

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.button = self.font.render(self.text, True, BLUE)
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            self.button = self.font.render(self.text, True, BLACK)
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

    def draw(self):
        self.screen.blit(self.button, self.rect)