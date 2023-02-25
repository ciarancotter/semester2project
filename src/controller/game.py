import pygame
import sys
import os

sys.path.append(os.path.abspath("./src"))
from model.gameobjects.game_interface import PlatformerGame
from view.gameui.scene import MainMenuScene, GameScene, LoadingScene
from model.gameobjects.public_enums import Movement, GameState

try:
    from pykinect2 import PyKinectV2
    from shared_memory_dict import SharedMemoryDict
    KINECT = True
    print("kinect connected")
except ImportError:
    KINECT = False


# key controls
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_a,
    K_s,
)

def main() -> None:
    # Initialize pygame
    pygame.init()
    running = True
    game_ran = False

    if KINECT:  
        # init shared memeory pool  
        movementPoolRead = SharedMemoryDict(name='movementPoolRead', size=1024) 
        movementPoolMisc = SharedMemoryDict(name='movementPoolMisc', size=1024) 
        # start python  


    clock = pygame.time.Clock()
    
    global_screen = pygame.display.set_mode((1280, 784))
    game_manager = PlatformerGame()
    main_menu_scene = MainMenuScene(game_manager, global_screen)
    loading_scene = LoadingScene(global_screen)
    game_scene = GameScene(game_manager, global_screen, loading_scene)
    main_menu_scene.initialise() # Loads up the menu scene
    game_manager.create_level_from_json()

    # Main game loop
    while running:

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

            if event.type == pygame.MOUSEBUTTONUP:
                main_menu_scene.check_play_pressed(event, game_scene)
                main_menu_scene.check_about_pressed(event)

        keys_pressed = pygame.key.get_pressed()
        movements_for_model = []

        # Controls
        if KINECT:
            if movementPoolMisc["turnleft"]:
                movements_for_model.append(Movement.left)
            elif movementPoolMisc["turnright"]:
                movements_for_model.append(Movement.right)
            elif movementPoolRead["jump"]:
                movements_for_model.append(Movement.jump)
            elif movementPoolRead["leftpunch"]:
                movements_for_model.append(Movement.left_punch)
            elif movementPoolRead["rightpunch"]:
                movements_for_model.append(Movement.right_punch)
            else:
                movements_for_model.append(Movement.no_movement)

        else:
            if keys_pressed[K_LEFT]:
                movements_for_model.append(Movement.left)
            elif keys_pressed[K_RIGHT]:
                movements_for_model.append(Movement.right)
            elif keys_pressed[K_UP]:
                movements_for_model.append(Movement.jump)
            elif keys_pressed[K_a]:
                movements_for_model.append(Movement.left_punch)
            elif keys_pressed[K_s]:
                movements_for_model.append(Movement.right_punch)
            else:
                movements_for_model.append(Movement.no_movement)
        

        if game_manager._gamestate == GameState.start_menu:
            main_menu_scene.checking_hover(pygame.mouse.get_pos())
            main_menu_scene.update() 
            pygame.display.flip()

        elif game_manager._gamestate == GameState.in_session:
            game_manager.update_model(movements_for_model)
            game_scene.update()
            pygame.display.flip()

    # Exit pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
