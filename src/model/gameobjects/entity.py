"""Class definition for the Entity and Player objects.

The Entity class is the parent class of the Player and Enemy classes,
and any other object on the canvas.

Usage:
    test_entity = Entity((20, 20), 30, 30, True)
    object_can_collide = test_entity.isColliding()
"""
import sys
import os
import random
import math
sys.path.append(os.path.abspath("./src"))
from .public_enums import Movement


class Entity:

    def __init__(self, xPos: int, yPos: int, width: int, height: int,
                 colliding: bool) -> None:
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

        # creating the hitbox
        self._hitbox_x_offset = 0
        self._hitbox_y_offset = 0
        self._hitbox_width_reduction = 0
        self._hitbox_height_reduction = 0

    def set_x(self, newX: int) -> None:
        """Setter method for the x-coordinate.
        """
        self.xPos = newX

    def set_y(self, newY: int) -> None:
        """Setter method for the y-coordinate.
        """
        self.yPos = newY

    def get_x(self) -> int:
        return self.xPos

    def get_y(self) -> int:
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

    def is_colliding_with_entity(self, entity):
        if ((entity.x+entity._hitbox_x_offset) + (entity.width-entity._hitbox_width_reduction) < self.xPos) or ((self.xPos + self._hitbox_x_offset) + (self._width-self._hitbox_width_reduction) < (entity.x+entity._hitbox_x_offset)):
            return False
        if ((entity.y+entity._hitbox_y_offset) + (entity.height-entity._hitbox_height_reduction) < (self.yPos+self._hitbox_y_offset)) or ((self.yPos+self._hitbox_y_offset) + (self._height-self._hitbox_height_reduction) < (entity.y+entity._hitbox_y_offset)):
            return False
        return True


    def is_colliding_with_entitys(self, entities: list) -> bool:
        """checks if this entity is colliding with anything in the list of 
        entitys provided.
        
        Args:
            entities: a list of entities to check for collitions with

        Returns: a boolean which is True if there is a collision and False
                if not

        """

        for entity in entities:
           if self.is_colliding_entity(entity):
            return True
        return False

    x = property(get_x, set_x)
    y = property(get_y, set_y)
    coordinates = property(get_coordinates)
    width = property(get_width)
    height = property(get_height)
    is_colliding_entity = property(is_colliding_entity)


class Block(Entity):
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

    def __init__(self, xPos: int, yPos: int, width: int, height: int) -> None:
        super().__init__(xPos, yPos, width, height, True)

class Door(Block):
    """An entity that sends you to a differnt level on contact.
    """

    def __init__(self, xPos: int, yPos: int, width: int, height: int):
        """Inits the Door class.
        """
        super().__init__(xPos, yPos, width, height)
        self._hitbox_width_reduction = 10

    def check_for_entry(self, player) -> bool:
        """Checks if the door has been entered.

            Returns: True if entered false if not 
        """
        if super().is_colliding_with_entity(player) == True:
            return True
        return False


class Monke(Entity):
    """ a class that represents a Monke like entity on the screen
    """

    def __init__(self, xPos: int, yPos: int, width: int, height: int,
                 colliding: bool, speed: int) -> None:
        self._speed = speed
        self._fall_speed = 5
        super().__init__(self.xPos, self.yPos, width, height, True)

    def collideTop(self, entities: list[Entity]) -> bool:
        """collideTop is an internal method that checks if the Monke is on top of a block.

        Args: 
            blocks: a list of block objects representing the block platforms on the screen 
            that can be stood on.

        Returns: True if the Monke is standing on a platform and False if not.

        """
        for entity in entities:
            if isinstance(entity, Block):
                monke_feet = (self.yPos+self._hitbox_y_offset) + (self._height-self._hitbox_height_reduction)
                check_above = not (monke_feet <= entity.yPos)
                check_below = (monke_feet <= entity.yPos + entity._height)
                check_left = (not ((self.xPos+self._hitbox_x_offset) + (self._width - self._hitbox_width_reduction) < entity.xPos))
                check_right = ((self.xPos+self._hitbox_x_offset) <= entity.xPos + entity._width)
            if (check_below and check_above and check_left and check_right):
                return True
        return False

    def gravity(self, entities: list[Entity]) -> bool:
        """if monke let go of tree it fall.
        """
        for i in range(self._fall_speed):
            if self.check_no_hit(entities):
                self.yPos += 1
                continue
            return False
        return True

    def check_no_hit(self, blocks: list[Entity]) -> None:
        """checks if the Monke has hit the top of the block or the ground.

            Args:
                blocks: a list of blocks of type Block
            Returns: True If you have not hit the top of the block or the ground.
        """

        return not ((self.yPos >= self.screen_height - self._height) or (
            self.collideTop(blocks)))


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

    def __init__(self, width: int, height: int, SCREEN_WIDTH: int, SCREEN_HEIGHT: int) -> None:
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.facing = Movement.left
        # start in the center of the screen and fall down
        self.xPos = SCREEN_WIDTH / 2
        self.yPos = SCREEN_HEIGHT / 2
        self._jump_baseline = self.yPos
        self._jump_height = 100
        self._jumped = True
        self._jumping = False
        self._jump_power = 50
        self._health = 10
        self.current_loot = None
        self._invincible = False

        super().__init__(self.xPos, self.yPos, width, height, True, 2)
        self._hitbox_x_offset = 15
        self._hitbox_y_offset = 10
        self._hitbox_width_reduction = 35
        self._hitbox_height_reduction = 10

    def move(self, directions: list[Movement], entities: list[Entity]) -> None:
        """this method is called to change the state of the player.

        this method is called to change the state of the player and does not have to 
        be in response to a movement. (no movement is an option) 

        Args:
            direction: direction of type Movement(enum) that indicates the direction the
                        player is to move.  

        """
        if directions == [Movement.no_movement]:
            self.facing = Movement.no_movement
        for direction in directions:
            #punching 
            if direction == Movement.left_punch:
                self.facing = Movement.left_punch
            if direction == Movement.right_punch:
                self.facing = Movement.right_punch
            #move left
            if direction == Movement.left and self.xPos >= 0:
                self.xPos -= self._speed
                self.facing = Movement.left
            #move right
            if direction == Movement.right and self.xPos < self.screen_width - self._width:
                self.xPos += self._speed
                self.facing = Movement.right


            if (not self._jumping) and direction == Movement.jump:
                self._jumping = True
                self._jump_baseline = self.yPos
                
        # if the player is jumping create an ark
        if self._jumping:
            self.yPos -= self._jump_power
            self._jump_power -= 5

            # done to prevent overshooting the ground
            if self._jump_power <= -10:
                self._jump_power = -10

        # if no longer falling then reset jump stuff
        if not self.gravity(entities):
            self._jumping = False
            self._jump_baseline = self.yPos
            self._jump_power = 50

        self.calculate_collition_results(entities)
        self.update_loot_stats()

    def calculate_collition_results(self, entities):
        for i,entity in enumerate(entities):
            if isinstance(entity, Enemy) and (self.is_colliding_with_entity(entity)):
                if not self._invincible:
                    self._health -= entity._damage

            elif isinstance(entity, Loot) and (self.is_colliding_with_entity(entity)):
                self._health += entity.power

            if isinstance(entity, JumpLoot) and (self.is_colliding_with_entity(entity)):
                self.current_loot = entity
                # increasing the jump height because it hit the loot
                self._jump_height += entity.jump_increase
                # making the loot disapear when you hit it
                entities.pop(i)

            if isinstance(entity, InvicibilityLoot) and (self.is_colliding_with_entity(entity)):
                self.current_loot = entity
                self._invincible = True
                # making the loot disapear when you hit it
                entities.pop(i)


    def update_loot_stats(self):
        """stores whether the player has gained any special powers.
            
            creates a timer and decrements it each frame to store the time
            that the powers will run out.
        """
        if self.current_loot == None:
            return
        if isinstance(self.current_loot,JumpLoot):
            if self.current_loot.power_up_time <= 0:
                self._jump_height -= self.current_loot.jump_increase
                self.current_loot = None
            self.current_loot.power_up_time -= 1

        if isinstance(self.current_loot,InvicibilityLoot):
            if self.current_loot.power_up_time <= 0:
                self._invincible = False
                self.current_loot = None
            self.current_loot.power_up_time -= 1

            

    def get_health(self):
        return self._health

    def get_invincibility(self):
        return self._invincible

    isInvincable = property(get_invincibility)
    health = property(get_health)



class Enemy(Monke):
    """the enemy sprites that travel around the game deal damage to our innocent explorer
    inheretes from Monke
    Atributes:
        dammage: the amount of dammage that this enemy deal.

    """

    def __init__(self, width: int, height: int, SCREEN_WIDTH: int, SCREEN_HEIGHT: int, dammage: int, player:Player) -> None:
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self._damage = dammage
        self._speed = 0.5

        self.screen_width = SCREEN_WIDTH
        self.player = player
        self.distance_to_player = 0
        self.xPos = random.randint(0, SCREEN_WIDTH)
        self.yPos = 2
        self.choice_of_sprit = random.randint(0,3)


        self.facing = random.choice([Movement.right, Movement.left])
        super().__init__(self.xPos, self.yPos, width, height, True, 3)

    def get_dammage(self) -> int:
        return self._damage

    def move(self, frame_count, player_date ,entities: list[Entity]):
        self.gravity(entities)

        if not self.gravity(entities):
            self.distance_to_player = math.sqrt((player_date.xPos - self.xPos)**2 + (player_date.yPos - self.yPos)**2)

            #logic for following player 
            if int(self.distance_to_player) < 100:
                if player_date.xPos + (player_date.width/2) < self.xPos:
                    self.facing = Movement.left
                    self.xPos -= self._speed
                elif player_date.xPos > self.xPos + (self.width/2):
                    self.facing = Movement.right
                    self.xPos += self._speed
            else:
                if self.facing == Movement.left and self.xPos >= 0:
                    self.xPos -= self._speed
                elif self.facing == Movement.right and self.xPos < self.screen_width - self._width:
                    self.xPos += self._speed
                elif self.facing == Movement.left and self.xPos <= self._width:
                    self.facing = Movement.right
                elif self.facing == Movement.right and self.xPos >= self.screen_width - self._width:
                    self.facing = Movement.left 




class Loot(Entity):
    """the Loot class contains power ups that the player can gain once they colide with it.
        
    Atributes:
        power: the potency of the loot
    """
    def __init__(self,xPos: int, yPos: int, width: int, height: int,colliding: bool,power=2):
        self._power = power
        super().__init__(self.xPos, self.yPos, width, height, True)
    def get_power(self):
        return self._power
    power = property(get_power)

class JumpLoot(Loot):
    """loot that makes you jump higher.
        
        Atributes:
            jump_increase: the amoun that your jump height increases when you get the loot
            power_up_time: the time period that your increased jump height remains in place
    """
    def __init__(self,xPos: int, yPos: int, width: int, height: int,colliding: bool,power=2,jump_increase=10,time=1000):
        self._jump_increase = jump_increase
        self.power_up_time = time
        super().__init__(self.xPos, self.yPos, width, height, True,power=power)
    def get_jump_increase(self):
        return self._jump_increase
    jump_increase = property(get_jump_increase)
    #power_up_time= property(get_power_up_time)

class InvicibilityLoot(Loot):
    """loot that renders the player unable to be damaged by enemies for a particular period."""
    def __init__(self,xPos: int, yPos: int, width: int, height: int,colliding: bool,power=2,time=1000):
        self.power_up_time = time
        super().__init__(self.xPos, self.yPos, width, height, True,power=power)
