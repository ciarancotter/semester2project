"""Class definition for the Entity and Player objects.

The Entity class is the parent class of the Player and Enemy classes,
and any other object on the canvas.

Usage:
    test_entity = Entity((20, 20), 30, 30, True)
    object_can_collide = test_entity.isColliding()
"""

import pygame

from .public_enums import Movement,GameState


class Entity:

    def __init__(self, xPos:int,yPos:int, width: int, height: int, colliding: bool):
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


    def setX(self, newX: int):
        """Setter method for the x-coordinate.
        """
        self.xPos = newX

    def setY(self, newY: int):
        """Setter method for the y-coordinate.
        """
        self.yPos = newY

    def getCoordinates(self) -> tuple:
        """Getter method for the coordinates property.
        """
        return (self.xPos,self.yPos)

    def getWidth(self) -> int:
        """Getter method for the width property.
        """
        return self._width
    
    def getHeight(self) -> int:
        """Getter method for the height property.
        """
        return self._height

    def isColliding(self) -> bool:
        """Getter method for the colliding property.
        """
        return self.colliding

class Block:
    def __init__(self, entity: Entity):
        self.entity = entity


class Player(Entity):
    """Player is the class that is used to represent the main charicter in the game.

    this class stores the information about the player that is independent from the
    game engine implementation.

    this class inheretes from entity as it is an entity on a screen.

    Attributes:
        screen_width: the width of the game screen that is being used
        screen height: the height of the screen being used
        facing: the direction that the charicter is going in used for
                deciding which sprite to display in the view
        player_speed: how fast the player moves on the screen
        xPos: the x co-ordenate of the player on the game plane
                that will be displayed on the screen
        yPos: the y co-ordenate of the player on the game plane
                that will be displayed on the screen.



    """
    def __init__(self,width: int, height: int, SCREEN_WIDTH : int, SCREEN_HEIGHT : int):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.facing = Movement.left
        self.player_speed = 2
        # start in the center of the screen and fall down
        self.xPos = SCREEN_WIDTH/2 
        self.yPos = SCREEN_HEIGHT/2
        super().__init__(self.xPos,self.yPos,width,height,True)
        self._jump_baseline = self.yPos
        self._jump_height = 50
        self._decending = False


    def move(self,direction:Movement,blocks):
        """this method is called to change the state of the player.

        this method is called to change the state of the player and does not have to 
        be in response to a movement. (no movement is an option) 

        Args:
            direction: direction of type Movement(enum) that indicates the direction the
                        player is to move.  

        """
        #move left
        if direction == Movement.left and self.xPos >= 0 :
            self.xPos -= self.player_speed
            self.facing = Movement.left
        #move right
        if direction == Movement.right and self.xPos < self.screen_width - self._width :
            self.xPos += self.player_speed
            self.facing = Movement.right



        if direction == Movement.jump and (self._jump_baseline - self.yPos < self._jump_height):
            self.yPos -= self.player_speed*20
        elif (self._jump_baseline - self.yPos >= self._jump_height):
            self._decending = True

        check_no_hit = (self.yPos < self.screen_height - self._height) and (not (self.collideTop(blocks)))
        if self._decending == True:
            if check_no_hit: 
                self.yPos += self.player_speed
            else:
                self._decending = False
                self._jump_baseline = self.yPos

        #gravity code
        if check_no_hit:
            self.yPos += self.player_speed
            self._jump_baseline = self.yPos

    def collideTop(self,blocks) -> bool:
        """collideTop is an internal method that checks if the player is on top of a block.

        Args: 
            blocks: a list of block objects representing the block platforms on the screen 
            that can be stood on.

        Returns: True if the player is standing on a platform and False if not.

        """
        for block in blocks:
            player_feet = self.yPos+self._height
            check_above = (player_feet <= block.entity.yPos)
            check_below = (player_feet<=block.entity.yPos + block.entity._height)
            check_left = (not(self.xPos < block.entity.xPos))
            check_right = (self.xPos <= block.entity.xPos+block.entity._width)
            if (check_below and check_above and check_left and check_right):
                return True
        return False
