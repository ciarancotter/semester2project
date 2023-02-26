import pygame

class Fader:

    def __init__(self, scene_transition):
        self.alpha = 0
        self.fading = None
        self.scene_transition = cycle(scene_transition) # Creates an iterator
        self.current_transition_scene = next(self.scene_transition)

        screen_surface = pygame.display.get_surface().get_rect()
        self.fader = pygame.Surface(screen_surface.size)
        self.fader.fill((0, 0, 0))

    def fade(self, screen):
        # self.scene.draw(screen)
        if self.fading:
            self.fader.set_alpha(self.alpha)
            screen.blit(self.fader, (0, 0))
