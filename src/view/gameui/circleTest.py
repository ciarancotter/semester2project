import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the circle
circle_radius = 50
circle_color = (255, 0, 0)
circle_position = (screen_width // 2, screen_height // 2)

# Draw the circle on a surface
circle_surface = pygame.Surface((circle_radius * 2, circle_radius * 2), pygame.SRCALPHA)
pygame.draw.circle(circle_surface, circle_color, (circle_radius, circle_radius), circle_radius)

# Blit the circle onto the screen
screen.blit(circle_surface, (circle_position[0] - circle_radius, circle_position[1] - circle_radius))

# Update the screen
pygame.display.update()

# Run the game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()