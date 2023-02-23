import pygame
import numpy as np
from shared_memory_dict import SharedMemoryDict

"""--------------Important Part---------------------------"""
video = SharedMemoryDict(name='movementVideo', size=500000)
"""-------------------------------------------------------"""

print(type(video["src"]))
# Convert the numpy array to a pygame surface
surface = pygame.surfarray.make_surface(video["src"])

# Display the pygame surface
pygame.init()
screen = pygame.display.set_mode((496, 279))
screen.blit(surface, (0, 0))
pygame.display.flip()

# Wait for the user to close the window
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    """--------------Important Part---------------------------"""
    surface = pygame.surfarray.make_surface(video["src"])
    screen.blit(surface, (0, 0))
    pygame.display.flip()
    """-------------------------------------------------------"""

pygame.quit()