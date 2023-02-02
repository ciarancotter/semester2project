import pygame
from view.gameui import uielements, healthbar
from model.aiutilities import aiutilities

# Initialize pygame and create a window
pygame.init()
dimensionX = 1280
dimensionY = 768
# aiutilities.configure_openai()
# legend = aiutilities.generate_monolith("tragic", "roman")

# get info about the screen we are using
infoobject = pygame.display.Info()
# Create the screen
screen = pygame.display.set_mode((dimensionX, dimensionY), pygame.HWSURFACE | pygame.DOUBLEBUF, 32)
# myTextBox = gameui.UITextBox(screen, 30, "monospace", 12)
# myTextBox.draw("Monke")

# myHealthBar = healthbar.HealthBar(100)
# myHealthBar.drawMaxHealth(screen)
# myHealthBar.drawCurrentHealth(screen, 100)

myGameWindow = uielements.GameWindow(screen)
myGameWindow.draw()

myElementWindow = uielements.ElementWindow(screen)
myElementWindow.draw(myGameWindow)

pygame.display.update()

# Main game loop
running = True
spacePressed = False
currentLine = 0

while running:
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and spacePressed == False:
                # if currentLine < len(legend):
                # myTextBox.erase()
                # myTextBox.draw(legend[currentLine])
                spacePressed = True
                currentLine += 1
                # myHealthBar.drawCurrentHealth(screen, (100 - 10 * currentLine))
                # else:
                # myTextBox.erase()
                # myTextBox.draw("End.")
                # break
            pygame.display.update()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                spacePressed = False

# Exit pygame
pygame.quit()
