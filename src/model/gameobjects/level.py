from model.gameobjects.entity import Block
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

    def __init__(self) -> None:
        self._blocks = []

    def add_block(self, row: int, column: int) -> None:
        """ add a block in a particular 28*28 blockspace
            
            Args:
                row:
                    a number between 0 and 27 defining which blockspace down from 
                    the top of the screen you wish to place your block.
                column:
                    a number between 0 and 27 defining which blockspace across from the
                    side you wish to place your block.
        """
        if ((0 <= row <= 27) and (0 <= column <= 27)):
            xMapping = row * 28
            yMapping = column * 28
            self._blocks.append(Block(xMapping, yMapping, 28, 28))

    def get_blocks(self) -> list[Block]:
        return self._blocks
