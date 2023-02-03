import pygame
from view.gameui import uielements, healthbar
from model.aiutilities import aiutilities

# Initialize pygame and create a window
pygame.init()

dimensionX = 1280
dimensionY = 768

aiutilities.configure_openai()
legend = aiutilities.generate_monolith("tragic", "roman")
print(legend)
# get info about the screen we are using
infoobject = pygame.display.Info()

# Create the screen
screen = pygame.display.set_mode((dimensionX, dimensionY), pygame.HWSURFACE | pygame.DOUBLEBUF, 32)

# Created some UI elements.
myGamePanel = uielements.Panel(screen, 768, 768, 0, 0, "blue")
myGamePanel.draw()

myUIPanel = uielements.Panel(screen, 512, 768, 768, 0, "black")
myUIPanel.draw()

myTextBox = uielements.TextBox(screen, 25, 25, "monospace", 12, myUIPanel)
myTextBox.draw("Monke")

myHealthBar = healthbar.HealthBar(screen, myGamePanel, 100)
myHealthBar.drawMaxHealth()
myHealthBar.drawCurrentHealth()

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

            elif event.key == pygame.K_SPACE and spacePressed == False:
                if currentLine < len(legend):

                  myTextBox.erase()
                  myTextBox.draw(legend[currentLine])

                  spacePressed = True
                  currentLine += 1

                  myHealthBar.reduceHealth(10)
                  myHealthBar.drawCurrentHealth()

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
