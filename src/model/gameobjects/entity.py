"""Class definition for the Entity object.

The Entity class is the parent class of the Player and Enemy classes,
and any other object on the canvas.

Usage:
    test_entity = Entity((20, 20), 30, 30, True)
    object_can_collide = test_entity.isColliding()
"""

import pygame

from game_interface import Movement


class Entity:

    def __init__(self, xPos:int,yPos:int, width: int, height: int, colliding: bool):
        """Inits the Entity object.

        Attributes:
            - coordinates: The object's position on the tilemap.
            - width: The width of the object.
            - height: The height of the object.
            - colliding: A boolean value that determines if the object collides with its environment.
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
    def __init__(self,width: int, height: int, SCREEN_WIDTH : int, SCREEN_HEIGHT : int):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.facing = Movement.left
        self.player_speed = 2
        self.xPos = SCREEN_WIDTH/2
        self.yPos = SCREEN_HEIGHT/2
        super().__init__(self.xPos,self.yPos,width,height,True)

    def move(self,direction:Movement,blocks):
        #move left
        if direction == Movement.left and self.xPos >= 0 :
            self.xPos -= self.player_speed
            self.facing = Movement.left
        #move right
        if direction == Movement.right and self.xPos < self.screen_width - self.width :
            self.xPos += self.player_speed
            self.facing = Movement.right

        #jumping when player on ground
        #TODO jumping in objects
        if direction == Movement.jump and self.yPos+self.height ==  self.screen_height :
            self.yPos -= self.player_speed*20



        #gravity code
        if (self.yPos < self.screen_height - self.height) and (not (self.collideTop(blocks))):
            self.xPos += self.player_speed

    def collideTop(self,blocks) -> bool:
        for block in blocks:
            player_feet = self.yPos+self._height
            check_above = (player_feet <= block.entity.yPos)
            check_below = (player_feet<=block.entity.yPos + block.entity._height)
            check_left = (not(self.xPos < block.entity.xPos))
            check_right = (self.xPos <= block.entity.xPos+block.entity._width)
            if (check_below and check_above and check_left and check_right):
                return True
        return False
