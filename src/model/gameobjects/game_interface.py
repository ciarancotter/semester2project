"""This is the module that a view would use to interact with a game object to get info about the game state.

This module contains 2 classes PlatformerGame and CtxToRender. PlatformerGame is the class that contains all
the information that is required store and update the gamestate(information about the game like charictar
position) from frame to frame. It returns CtxToRender which contains all the information needed to
display this gamestate to the user.

Typical usage example:

game = PlatformerGame()
ctx = game.get_render_ctx()
for block in ctx.blocks:
	print(block.coordinates)
# print the coordinates of all the blocks in the game
"""

import json
import random
from model.gameobjects.level import Level
from model.gameobjects.entity import *
from model.gameobjects.public_enums import Movement, GameState
from model.aiutilities.aiutilities import generate_monolith

class CtxToRender(object):

    def __init__(
            self, enemies: list[Enemy],
            player: Player,
            blocks: list[Block],
            entities: list[Entity],
            game_state: GameState,
            current_level: int,
            door: Door,
            monolith: Monolith
            ) -> None:

        """contains all the information needed to 
		display a gamestate to the user.

		meant to be used as a container to be passed to 
		a module using a game engine but attempts to be
		platform independent.

		Args:
			enemies: a list of enemy objects to be displayed
			on the screen
			player: a player object representing main charicter
			blocks: a list of block platforms
			entities: a list of all the perivios entities together 

		"""
        self._enemies = enemies
        self._player = player
        self._blocks = blocks
        self._entities = entities
        self._gamestate = game_state
        self._current_level = current_level
        self._door = door
        self._monolith = monolith

    def get_entities(self) -> list[Entity]:
        return self._entities

    def get_player(self) -> Player:
        return self._player
    
    def get_door(self) -> Door:
        return self._door

    def get_blocks(self) -> list[Block]:
        return self._blocks

    def get_enemies(self) -> list[Enemy]:
        return self._enemies

    def get_game_state(self) -> GameState:
        return self._gamestate
     
    def get_current_level(self) -> int:
        return self._current_level
    
    def get_monolith(self):
        return self._monolith


    enemies = property(get_enemies)
    player = property(get_player)
    door = property(get_door)
    blocks = property(get_blocks)
    entities = property(get_entities)
    game_state = property(get_game_state)
    current_level = property(get_current_level)
    monolith = property(get_monolith)


class PlatformerGame(object):
    """ The main game class that stores the gamestate.
    
        Attributes:
            - playerwidth: The width of the player.
            - playerheight: The height of the player.
            - screen_width: The width of the screen.
            - screen_height: The height of the screen.
            - current_level: The value of the current level.
            - enemies: The array of enemies in the game at the moment.
            - player: The Player object to interact with the game.
            - blocks: The blocks that are placed on the level.
            - entities: The Entity objects in the level.
            - gamestate: The enum that denotes the current scene.
            - punch_state: The check for a punch.
            - door: The door of the level.
    """

    def __init__(self) -> None:
        # initialise all the objects
        #door to be added
        self._playerwidth = 64
        self._playerheight = 64
        self._screen_width = 768
        self._screen_height = 768
        self._current_level = 1
        damage = 0 
        #xPos: int, yPos: int, width: int, SCREEN_WIDTH: int, SCREEN_HEIGHT: int, height: int,colliding: bool, dammage: int, player:Player) -> None:
        self._player = Player(self._playerwidth, self._playerheight,
                              self._screen_width, self._screen_height)
        self._enemy = Enemy(self._playerwidth, self._playerheight, 
                            self._screen_width, self._screen_height
                            ,damage ,self._player)
        self._enemies = [self._enemy]

        self._blocks = []
        self._entities = [self._enemies]
        self._gamestate = GameState.start_menu
        #punch state
        self._punch_state = False
        self._level_added = False
        self._door = None
        self._monolith = None
        self.frame_count = 0
        self._loot = []

    def get_render_ctx(self) -> CtxToRender:
        """Returns the information necicary (or the context/shortend to ctx in this program ) to render
		the game visualy.

		Returns:
			a CtxToRender object containing the necicary rendering information.

		"""
        return CtxToRender(
                self._enemies,
                self._player,
                self._blocks,
                self._entities,
                self._gamestate,
                self._current_level,
                self._door,
                self._monolith
                )


    def set_game_state(self, new_game_state):
        """Setter method for game state.
        """
        self._gamestate = new_game_state


    def update_model(self, player_moves: list(Movement)):
        self.frame_count +=1
        self._entities =  self._player.move(player_moves, self._entities)
        self._enemy.move(self.frame_count, self._blocks)

        if self._player.health <= 0:
            self.game_state = GameState.game_over

        self.add_powerups()

        if self._door != None and self._door.check_for_entry(self._player):
            self._level_added = True
            self._current_level += 1
            self.create_level_from_json()

        if self._monolith != None and self._monolith.check_for_read(self._player):
            self._monolith.is_being_read = True
        elif self._monolith != None and not self._monolith.check_for_read(self._player):
            self._monolith.is_being_read = False


    def create_level_from_json(self):
        """Finds out what level the game is on and then parses the json file to 
        get the information required to set up that level.
        """

        with open('src/model/gameobjects/level_info.json', 'r') as file:
            level_object = Level()
            self._level_added = False
            json_info = json.load(file)
            number_of_levels = len(json_info)
            new_level_number = random.randint(0, number_of_levels)
            # compiling the correct key to find the level information
            try:
                level = json_info[new_level_number - 1]
            except Exception as e:
                print(e)
                self._gamestate = GameState.game_over
                return

            self._door = Door(
                    level["door"]["x"] * 28,
                    level["door"]["y"] * 28, 
                    64,
                    64
                    )

            self._monolith = Monolith(
                    level["monolith"]["x"] * 28,
                    level["monolith"]["y"] * 28,
                    64,
                    64
                    )

            for block in level["blocks"]:
                level_object.add_block(block["x"],block["y"])

            # setting up the level information in this object
            self._blocks = level_object.get_blocks()

            self._entities = []
            self._entities.extend(level_object.get_blocks())
            self._player = Player(self._playerwidth, self._playerheight,
                             self._screen_width, self._screen_height)
            
            self._entities.append(self._player)
            self._entities.append(self._door)
            self._entities.append(self._monolith)


    def add_powerups(self):
        """adds powerups to the screen.

        adds powerups to the screen as long as it is not spawning ontop of an entity.
        """
        if self.frame_count % 1000:
            random_number = random.randint(0, 3)
            x = random.randint(0,self._screen_width)
            y = random.randint(0,self._screen_height)



            if random_number == 0:
                loot = Loot(x, y, 64, 64)
                if not loot.is_colliding_with_entitys(self._entities):
                    self._entities.append(loot)
                    self._loot.append(loot)
            elif random_number == 1:
                loot = JumpLoot(x, y, 64, 64)
                if not loot.is_colliding_with_entitys(self._entities):
                    self._entities.append(loot)
                    self._loot.append(loot)
            else:
                loot = InvicibilityLoot(x, y, 64, 64)
                if not loot.is_colliding_with_entitys(self._entities):
                    self._entities.append(loot)
                    self._loot.append(loot)










