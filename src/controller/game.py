import pygame
import sys
import os

sys.path.append(os.path.abspath("./src"))
from model.gameobjects.game_interface import PlatformerGame
from view.gameui.scene import MainMenuScene, GameScene, LoadingScene, AboutMenuScene
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
    K_SPACE,
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
    #self.leaderboard_scene = LeaderboardScene(global_screen)
    #self.help_scene = HelpScene(global_screen)
    about_scene = AboutMenuScene(game_manager, global_screen)
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
                main_menu_scene.check_play_pressed(event.pos, game_scene)
                main_menu_scene.check_about_pressed(event.pos, about_scene)
                about_scene.check_back_pressed(mouse_pos, main_menu_scene)

        keys_pressed = pygame.key.get_pressed()
        movements_for_model = []

        # Controls
        if KINECT:
            if movementPoolMisc["turnleft"]:
                movements_for_model.append(Movement.left)
            if movementPoolMisc["turnright"]:
                movements_for_model.append(Movement.right)
            if movementPoolRead["jump"]:
                movements_for_model.append(Movement.jump)
            if movementPoolRead["leftpunch"]:
                movements_for_model.append(Movement.left_punch)
            if movementPoolRead["rightpunch"]:
                movements_for_model.append(Movement.right_punch)
            if movements_for_model == []:
                movements_for_model = [Movement.no_movement]

        else:
            if keys_pressed[K_LEFT]:
                movements_for_model.append(Movement.left)
            if keys_pressed[K_RIGHT]:
                movements_for_model.append(Movement.right)
            if keys_pressed[K_UP] or keys_pressed[K_SPACE]:
                movements_for_model.append(Movement.jump)
            if keys_pressed[K_a]:
                movements_for_model.append(Movement.left_punch)
            if keys_pressed[K_s]:
                movements_for_model.append(Movement.right_punch)
            else:
                movements_for_model.append(Movement.no_movement)

        # handles cursor in the menu
        pygame.mouse.set_visible(False)
        pygame.mouse.set_cursor(pygame.cursors.diamond)
        mouse_pos = pygame.mouse.get_pos()
        if KINECT:
            if movementPoolMisc["mousex"] > 0:
                if movementPoolMisc["mousey"] > 0:
                    mouse_pos = (int(movementPoolMisc["mousex"]), int(movementPoolMisc["mousey"]))
        
        if game_manager._gamestate == GameState.start_menu:
            if KINECT and movementPoolRead["select"]:
                main_menu_scene.check_play_pressed(mouse_pos, game_scene)
                main_menu_scene.check_about_pressed(mouse_pos, about_scene)
            main_menu_scene.checking_hover(mouse_pos)
            main_menu_scene.update() 
            main_menu_scene.draw_cursor(mouse_pos)

        elif game_manager._gamestate == GameState.in_session:
            game_manager.update_model(movements_for_model)
            game_scene.update()

        elif game_manager._gamestate == GameState.about:
            if KINECT and movementPoolRead["select"]:
                about_scene.check_back_pressed(mouse_pos, main_menu_scene)
            about_scene.checking_hover(mouse_pos)
            about_scene.update() 
            about_scene.draw_cursor(mouse_pos)

        # refresh entire screen
        pygame.display.flip()
        #print(round(clock.get_fps(), 2))

    # Exit pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
