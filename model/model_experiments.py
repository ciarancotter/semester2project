import pygame
from aiutilities import aiutilities
from gameui import gameui

# Initialize pygame and create a window
pygame.init()
dimensions = 512

aiutilities.configure_openai()
legend = aiutilities.generate_monolith("tragic", "roman")

screen = pygame.display.set_mode((dimensions, dimensions))
myTextBox = gameui.UITextBox(screen, 30, "monospace", 12)
myTextBox.draw("Monke")
pygame.display.update()

# Main game loop
running = True
spacePressed = False
currentLine = 0

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and spacePressed == False:
                if currentLine < len(legend):
                    myTextBox.erase()
                    myTextBox.draw(legend[currentLine])
                    spacePressed = True
                    currentLine += 1
                else:
                    myTextBox.erase()
                    myTextBox.draw("End.")
                    break
            pygame.display.update()
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                spacePressed = False
                

# Exit pygame
pygame.quit()


        