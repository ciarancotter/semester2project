"""Class definition for the Entity object.

The Entity class is the parent class of the Player and Enemy classes,
and any other object on the canvas.

Usage:
    test_entity = Entity((20, 20), 30, 30, True)
    object_can_collide = test_entity.isColliding()
"""

import pygame

class Entity:

    def __init__(self, coordinates: tuple, width: int, height: int, colliding: bool):
        """Inits the Entity object.

        Attributes:
            - coordinates: The object's position on the tilemap.
            - width: The width of the object.
            - height: The height of the object.
            - colliding: A boolean value that determines if the object collides with its environment.
        """
        self.coordinates: tuple = coordinates 
        self.colliding: bool = colliding
        self._width: int = width
        self._height: int = height


    def setX(self, newX: int):
        """Setter method for the x-coordinate.
        """
        self.coordinates[0] = newX

    def setY(self, newY: int):
        """Setter method for the y-coordinate.
        """
        self.coordinates[1] = newY

    def getCoordinates(self) -> tuple:
        """Getter method for the coordinates property.
        """
        return self.coordinates

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
