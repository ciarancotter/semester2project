"""Class definition for the Entity and Player objects.

The Entity class is the parent class of the Player and Enemy classes,
and any other object on the canvas.

Usage:
    test_entity = Entity((20, 20), 30, 30, True)
    object_can_collide = test_entity.isColliding()
"""
import sys
import os

sys.path.append(os.path.abspath("./src"))
from .public_enums import Movement, GameState


class Entity:

    def __init__(self, xPos: int, yPos: int, width: int, height: int,
                 colliding: bool):
        """Inits the Entity object.

        Attributes:
            coordinates: The object's position on the tilemap.
            width: The width of the object.
            height: The height of the object.
            xPos: the x co-ordenate of the entity on the game plane
                that will be displayed on the screen
            yPos: the y co-ordenate of the entity on the game plane
                that will be displayed on the screen.

        """
        self.colliding: bool = colliding
        self._width: int = width
        self._height: int = height
        self.xPos = xPos
        self.yPos = yPos

    def set_x(self, newX: int):
        """Setter method for the x-coordinate.
        """
        self.xPos = newX

    def set_y(self, newY: int):
        """Setter method for the y-coordinate.
        """
        self.yPos = newY

    def get_x(self):
        return self.xPos

    def get_y(self):
        return self.yPos

    def get_coordinates(self) -> tuple:
        """Getter method for the coordinates property.
        """
        return (self.xPos, self.yPos)

    def get_width(self) -> int:
        """Getter method for the width property.
        """
        return self._width

    def get_height(self) -> int:
        """Getter method for the height property.
        """
        return self._height

    def is_colliding_entity(self) -> bool:
        """Getter method for the colliding property.
        """
        return self.colliding

    def is_colliding_with_entity(self, entities: list) -> bool:
        """checks if this entity is colliding with anything in the list of 
        entitys provided.
        
        Args:
            entities: a list of entities to check for collitions with

        Returns: a boolean which is True if there is a collision and False
                if not

        """

        for entity in entities:
            # check if one rectangle is to the left of an other
            if (entity.x + entity.width < self.xPos) or (self.xPos + self._width
                                                         < entity.x):
                continue
            # check if one rectangle is on top of an other
            if (entity.y + entity.height <
                    self.yPos) or (self.yPos + self._height < entity.y):
                continue
            return True
        return False

    x = property(get_x, set_x)
    y = property(get_y, set_y)
    coordinates = property(get_coordinates)
    width = property(get_width)
    height = property(get_height)
    is_colliding_entity = property(is_colliding_entity)


class Block:
    """An entity platform that sprites can stand on.

    Attributes:
            coordinates: The object's position on the tilemap.
            width: The width of the object.
            height: The height of the object.
            xPos: the x co-ordenate of the entity on the game plane
                that will be displayed on the screen
            yPos: the y co-ordenate of the entity on the game plane
                that will be displayed on the screen.

    """

    def __init__(self, xPos: int, yPos: int, width: int, height: int):
        super().__init__(self.xPos, self.yPos, width, height, True)


class Monke(Entity):
    """ a class that represents a Monke like entity on the screen
    """

    def __init__(self, xPos: int, yPos: int, width: int, height: int,
                 colliding: bool, speed: int):
        self._speed = speed
        super().__init__(self.xPos, self.yPos, width, height, True)

    def collideTop(self, entities) -> bool:
        """collideTop is an internal method that checks if the Monke is on top of a block.

        Args: 
            blocks: a list of block objects representing the block platforms on the screen 
            that can be stood on.

        Returns: True if the Monke is standing on a platform and False if not.

        """
        for entity in entities:
            if isinstance(entity, Block):
                monke_feet = self.yPos + self._height
                check_above = not (monke_feet <= entity.yPos)
                check_below = (monke_feet <= entity.yPos + entity._height)
                check_left = (not (self.xPos + self._width < block.xPos))
                check_right = (self.xPos <= entity.xPos + entity._width)
            if (check_below and check_above and check_left and check_right):
                return True
        return False

    def gravity(self, entities):
        """if monke let go of tree it fall.
        """
        if self.check_no_hit(entities):
            self.yPos += self._speed
            return True
        return False

    def check_no_hit(self, blocks):
        """checks if the Monke has hit the top of the block or the ground.

            Args:
                blocks: a list of blocks of type Block
            Returns: True If you have not hit the top of the block or the ground.
        """
        return (self.yPos < self.screen_height - self._height) and (
            not (self.collideTop(blocks)))


class Player(Monke):
    """Player is the class that is used to represent the main charicter in the game.

    this class stores the information about the player that is independent from the
    game engine implementation.

    this class inheretes from entity as it is an entity on a screen.

    Attributes:
        screen_width: the width of the game screen that is being used
        screen height: the height of the screen being used
        facing: the direction that the charicter is going in used for
                deciding which sprite to display in the view
        _player: how fast the player moves on the screen
        xPos: the x co-ordenate of the player on the game plane
                that will be displayed on the screen
        yPos: the y co-ordenate of the player on the game plane
                that will be displayed on the screen.



    """

    def __init__(self, width: int, height: int, SCREEN_WIDTH: int,
                 SCREEN_HEIGHT: int):
        super().__init__(self.xPos, self.yPos, width, height, True, 2)
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.facing = Movement.left
        # start in the center of the screen and fall down
        self.xPos = SCREEN_WIDTH / 2
        self.yPos = SCREEN_HEIGHT / 2
        self._jump_baseline = self.yPos
        self._jump_height = 50
        self._jumped = True
        self._health = 10

    def move(self, direction: Movement, entities):
        """this method is called to change the state of the player.

        this method is called to change the state of the player and does not have to 
        be in response to a movement. (no movement is an option) 

        Args:
            direction: direction of type Movement(enum) that indicates the direction the
                        player is to move.  

        """
        #move left
        if direction == Movement.left and self.xPos >= 0:
            self.xPos -= self._speed
            self.facing = Movement.left
        #move right
        if direction == Movement.right and self.xPos < self.screen_width - self._width:
            self.xPos += self._player
            self.facing = Movement.right

        if direction == Movement.jump and (
            (self._jump_baseline - self.yPos < self._jump_height) and
                not self._jumped):
            self.yPos -= self._player * 20
        elif (self._jump_baseline - self.yPos >= self._jump_height):
            self._jumped = True

        if self._jumped == True:
            if self.check_no_hit(entities):
                self.yPos += self._player
            else:
                self._jumped = False
                self._jump_baseline = self.yPos

        if not self.gravity(entities):
            self._jump_baseline = self.yPos
            jumped = False
        self.calculate_damage(entities)

    def calculate_damage(self, entities):
        for entity in entities:
            if isinstance(entity, Enemy) and (self.is_colliding_entity(entity)):
                self._health -= entity._damage

    def get_health(self):
        return self._health

    health = property(get_health)


class Enemy(Monke):
    """the enemy sprites that travel around the game deal damage to our innocent explorer
    inheretes from Monke
    Atributes:
        dammage: the amount of dammage that this enemy deal.

    """

    def __init__(self, xPos: int, yPos: int, width: int, height: int,
                 colliding: bool, dammage: int):
        super().__init__(self.xPos, self.yPos, width, height, True)
        self._damage = dammage

    def get_dammage(self):
        return self._damage

    def move(self, entities):
        self.gravity(entities)
        #TODO: add autonomous movement

    damage = property(get_dammage)
