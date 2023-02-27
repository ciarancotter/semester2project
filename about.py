import pygame
pygame.init()

WINDOW_SIZE = (1280, 780)
screen = pygame.display.set_mode(WINDOW_SIZE)

background_image = pygame.image.load("src/view/assets/aboutBG.png")

logo = pygame.image.load("src/view/assets/logo.png")
logo = pygame.transform.scale(logo, (800, 150))

black = (0, 0, 0)
white = (255, 255, 255)

bradley = pygame.image.load("src/view/assets/profiles/bradleyAbout.png")
samina = pygame.image.load("src/view/assets/profiles/saminaAbout.png")
ciaran = pygame.image.load("src/view/assets/profiles/ciaranAbout.png")
niamh = pygame.image.load("src/view/assets/profiles/niamhAbout.png")
shaza = pygame.image.load("src/view/assets/profiles/shazaAbout.png")
patrick = pygame.image.load("src/view/assets/profiles/patrickAbout.png")

# Create a list of the images
images = [bradley, samina, ciaran, niamh, shaza, patrick]

# Set the dimensions and positions of the images
image_width = 200
image_height = 200
image_spacing = 20
image_x1 = 0
image_x2 = 640
image_y1 = 150
image_y2 = 150

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("About")

clock = pygame.time.Clock()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill(white)

    window.blit(background_image, (0, 0))

    for i in range(len(images)):
        if i < 3:
            x = image_x1
            y = image_y1 + (image_height + image_spacing) * i
        else:
            x = image_x2
            y = image_y2 + (image_height + image_spacing) * (i - 3)
        window.blit(images[i], (x, y))


        logo_x_pos = (WINDOW_SIZE[0] - logo.get_width()) // 2

        screen.blit(logo, (logo_x_pos, 20))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
