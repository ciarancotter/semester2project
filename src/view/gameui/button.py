class Button:
    def __init__(self, screen, font, text, position):
        self.screen = screen
        self.font = font
        self.text = text
        self.position = position
        self.BLACK = (0, 0, 0)
        self.BLUE = (104, 119, 225)
        self.render_text()

    def render_text(self):
        self.button = self.font.render(self.text, True, self.BLACK)
        self.rect = self.button.get_rect()
        self.rect.center = self.position

    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.button = self.font.render(self.text, True, self.BLUE)
        else:
            self.button = self.font.render(self.text, True, self.BLACK)

    def draw(self):
        self.screen.blit(self.button, self.rect)
