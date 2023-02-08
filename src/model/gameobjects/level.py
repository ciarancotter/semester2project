import pygame
from entity import Block
"""This file contains the code that controls the levels layout.

Typical ussage example:
    level1 = level()
    level1.add_block(1,3)
    level1.add_block(10,12)
    blocks = level1.get_blocks()
""" 
class level(object):
    """level contains all the blocks in the level 
    and provides an interface to set and get them
    """
    def __init__(self):
        self._blocks = []
    def add_block(self, row, column):
        """ add a block in a particular 32*32 blockspace
            
            Args:
                row:
                    a number between 0 and 31 defining which blockspace down from 
                    the top of the screen you wish to place your block.
                column:
                    a number between 0 and 31 defining which blockspace across from the
                    side you wish to place your block.
        """
        if ((0<=row<=31)and (0<=column<=31)):
            xMapping = row*32
            yMapping = column*32
            block_entitiy = Entity(xMapping,yMapping,32,32,True)
            self._blocks.append(Block(block_entitiy))
    def get_blocks(self):
        return self._blocks