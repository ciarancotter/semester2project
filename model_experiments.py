import pygame
from view.gameui import chatbox, healthbar
from model.aiutilities import textai

# Initialize pygame and create a window
pygame.init()
dimensions = 512

textai.configure_openai()
legend = textai.generate_monolith("tragic", "roman")

screen = pygame.display.set_mode((dimensions, dimensions))
myTextBox = chatbox.UITextBox(screen, 30, "monospace", 12)
myTextBox.draw("Monke")

myHealthBar = healthbar.HealthBar(100)
myHealthBar.drawMaxHealth(screen)
myHealthBar.drawCurrentHealth(screen, 100)

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
                    myHealthBar.drawCurrentHealth(screen,
                                                  (100 - 10 * currentLine))
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