import pygame
pygame.init()

WINDOW_SIZE = (1280, 780)
screen = pygame.display.set_mode(WINDOW_SIZE)

background_image = pygame.image.load("src/view/assets/aboutBG.png")
background_rect = background_image.get_rect()

logo = pygame.image.load("src/view/assets/logo.png")
logo = pygame.transform.scale(logo, (800, 150))

black = (0, 0, 0)
white = (255, 255, 255)
gold = (255, 215, 0)

bradley = pygame.image.load("src/view/assets/profiles/bradleyAbout.png")
niamh = pygame.image.load("src/view/assets/profiles/niamhAbout.png")
ciaran = pygame.image.load("src/view/assets/profiles/ciaranAbout.png")
samina = pygame.image.load("src/view/assets/profiles/saminaAbout.png")
shaza = pygame.image.load("src/view/assets/profiles/shazaAbout.png")
patrick = pygame.image.load("src/view/assets/profiles/patrickAbout.png")

bradley_description="Bradley Harris"
samina_description="Samina Arshad"
niamh_description="Niamh Connolly"
shaza_description="Shaza"
ciaran_description="Ciaran Cotter"
patrick_description="Patrick Lenhian"

bradley_role="Developer"
samina_role="Developer"
niamh_role="Developer"
shaza_role="Developer"
ciaran_role="Developer"
patrick_role="Developer"

# Set the dimensions and positions of the images and developer names
'''image_width = 100
image_height = 100
image_spacing = 20
image_x1 = 0
image_x2 = 320
image_y1 = 300
image_y2 = 300
font_color = black'''

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("About")

clock = pygame.time.Clock()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill(white)

    window.blit(background_image, background_rect)

    # Draw a gold square with rounded corners under the developers
    square_position = (0, 190)
    square_size = (700, 500)
    border_radius = 20
    pygame.draw.rect(screen, (gold), (square_position, square_size), border_radius=border_radius)

    # Add text to the gold square
    font = pygame.font.SysFont("monospace", 72, bold=True)
    text = "MEET THE TEAM"
    text_surface = font.render(text, True, black, gold)
    text_rect = text_surface.get_rect()
    text_rect.center = ((square_position[0] + square_size[0]) // 2, square_position[1] + 50)
    screen.blit(text_surface, text_rect)

    # Draw a black border around the square
    border_position = (square_position[0] - 5, square_position[1] - 5)
    border_size = (square_size[0] + 10, square_size[1] + 10)
    border_radius = 20
    pygame.draw.rect(screen, (black), (border_position, border_size), 5, border_radius=border_radius)

    # Define the position and size of the text box
    text_box_position = (800, 190)
    text_box_size = (410, 300) 


    # Define the font and color for the text
    font = pygame.font.SysFont("monospace", 18, bold=True)

    # Create a surface with the desired text
    long_sentence = "Welcome to Boole Raider! This is a camera recognition game which allows you to lead the character in the game and go through the levels with your own movements! We are a group of computer scientist students that have created this game for their software engineering project at UCC in the college year of 2022-2023. Click HELP on the main menu to learn how to play!"
    text_surface = font.render(long_sentence, True, black)

    # Wrap the text in a box of 400px width
    lines = []
    while long_sentence:
        i = 1
        # Find the maximum number of characters that fit in the 400px width
        while font.size(long_sentence[:i])[0] < 400 and i < len(long_sentence):
            i += 1
        # If the entire sentence fits within the 400px width, add it as a line
        if i == len(long_sentence):
            lines.append(long_sentence)
            long_sentence = ""
        else:
            # Find the last space within the 400px width to split the line
            if " " in long_sentence[:i]:
                i = long_sentence[:i].rfind(" ") + 1
            # Add the line to the list
            lines.append(long_sentence[:i])
            long_sentence = long_sentence[i:]

    # Create a surface for the text box with a gold background
    text_box_surface = pygame.Surface(text_box_size)
    text_box_surface.fill(gold)

    # Blit the wrapped text surface onto the text box surface
    y = 10
    for line in lines:
        text_surface = font.render(line, True, black, gold)
        text_box_surface.blit(text_surface, (10, y))
        y += text_surface.get_height() + 5

    # Create a surface for the black border
    border_surface = pygame.Surface((text_box_size[0] + 10, text_box_size[1] + 10))
    border_surface.fill(black)

    # Draw the gold text box on top of the border surface
    border_surface.blit(text_box_surface, (5, 5))

    # Draw the black border with rounded corners on top of the gold text box
    border_rect = pygame.draw.rect(border_surface, black, (0, 0, text_box_size[0]+10, text_box_size[1]+10), 5, border_radius=10)

    # Blit the border surface onto the main window surface
    window.blit(border_surface, text_box_position)

    # draw item images and descriptions
    font = pygame.font.SysFont("monospace", 24, bold=True)
    screen.blit(bradley, (0, 280))
    bradley_text = font.render(bradley_description, True, (0,0,0))
    screen.blit(bradley_text, (120, 350))
    bradley_text2 = font.render(bradley_role, True, (0,0,0))
    screen.blit(bradley_text2, (120, 380))

    screen.blit(niamh, (0, 420))
    niamh_text = font.render(niamh_description, True, (0,0,0))
    screen.blit(niamh_text, (120, 470))
    niamh_text2 = font.render(niamh_role, True, (0,0,0))
    screen.blit(niamh_text2, (120, 500))

    screen.blit(ciaran, (0, 540))
    ciaran_text = font.render(ciaran_description, True, (0,0,0))
    screen.blit(ciaran_text, (120, 600))
    ciaran_text2 = font.render(ciaran_role, True, (0,0,0))
    screen.blit(ciaran_text2, (120, 630))

    screen.blit(samina, (320, 300))
    samina_text = font.render(samina_description, True, (0,0,0))
    screen.blit(samina_text, (450, 350))
    samina_text2 = font.render(samina_role, True, (0,0,0))
    screen.blit(samina_text2, (450, 380))

    screen.blit(shaza, (320, 420))
    shaza_text = font.render(shaza_description, True, (0,0,0))
    screen.blit(shaza_text, (450, 470))
    shaza_text2 = font.render(shaza_role, True, (0,0,0))
    screen.blit(shaza_text2, (450, 500))

    screen.blit(patrick, (320, 540))
    patrick_text = font.render(patrick_description, True, (0,0,0))
    screen.blit(patrick_text, (450, 600))
    patrick_text2 = font.render(patrick_role, True, (0,0,0))
    screen.blit(patrick_text2, (450, 630))
    

    logo_x_pos = (WINDOW_SIZE[0] - logo.get_width()) // 2

    screen.blit(logo, (logo_x_pos, 20))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
