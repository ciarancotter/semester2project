import pygame

pygame.init()

WINDOW_SIZE = (1280, 780)
screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption("Meet the team")

background = pygame.image.load("src/view/assets/aboutBG.png")

logo = pygame.image.load("src/view/assets/logo.png")
logo = pygame.transform.scale(logo, (800, 150))

# Load the images and create a dictionary of their roles
images = {
    "Bradley Harris": {"image": pygame.image.load("src/view/assets/profiles/bradleyAbout.png"), "role": "Back-end Developer"},
    "Samina Arshad": {"image": pygame.image.load("src/view/assets/profiles/saminaAbout.png"), "role": "Back-end Devloper"},
    "Ciaran Cotter": {"image": pygame.image.load("src/view/assets/profiles/ciaranAbout.png"), "role": "Back-end Developer"},
    "Niamh Connolly": {"image": pygame.image.load("src/view/assets/profiles/niamhAbout.png"), "role": "Back-end Developer"},
    "Shaza Aldawamneh": {"image": pygame.image.load("src/view/assets/profiles/shazaAbout.png"), "role": "Back-end Devloper"},
    "Patrick Lenihen": {"image": pygame.image.load("src/view/assets/profiles/patrickAbout.png"), "role": "Back-end Devloper"}
}

# Define the positions of the images and text
left_x_pos = 50
right_x_pos = 750
y_pos = 200  
spacing = 30

font = pygame.font.Font(None, 36)

screen.blit(background, (0, 0))
# Calculate the x-position for the center of the logo image
logo_x_pos = (WINDOW_SIZE[0] - logo.get_width()) // 2
# Draw the logo image at the top of the screen
screen.blit(logo, (logo_x_pos, 20))

for i, (name, data) in enumerate(images.items()):
    # Determine which column to place the image and text in
    if i < 3:
        x_pos = left_x_pos
    else:
        x_pos = right_x_pos
    
    # Draw the image
    screen.blit(data["image"], (x_pos, y_pos))
    
    # Draw the name and role
    name_text = font.render(name.capitalize(), True, (255, 255, 255))
    role_text = font.render(data["role"], True, (255, 255, 255))
    screen.blit(name_text, (x_pos + data["image"].get_width() + spacing, y_pos))
    screen.blit(role_text, (x_pos + data["image"].get_width() + spacing, y_pos + 30))
    
    # Increase the y position for the next image and text
    if i == 2:
        y_pos = 200  # Reset the position for the next column
    else:
        y_pos += data["image"].get_height() + spacing


pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()


# Define the positions of the images and text
left_x_pos = 50
right_x_pos = 750
y_pos = 200  
spacing = 30

font = pygame.font.Font(None, 36)

screen.blit(background, (0, 0))

# Calculate the x-position for the center of the logo image
logo_x_pos = (WINDOW_SIZE[0] - logo.get_width()) // 2

screen.blit(logo, (logo_x_pos, 20))

# Draw the images and text
for i, (role, image) in enumerate(images.items()):
    # Determine which column to place the image and text in
    if i < 3:
        x_pos = left_x_pos
    else:
        x_pos = right_x_pos

    # Draw the image
    screen.blit(image, (x_pos, y_pos))
    # Draw the text
    text = font.render(role.capitalize(), True, (255, 255, 255))
    screen.blit(text, (x_pos + image.get_width() + spacing, y_pos))
    
    # Increase the y position for the next image and text
    if i == 2:
        y_pos = 200
    else:
        y_pos += image.get_height() + spacing

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
