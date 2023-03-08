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

    def get_is_colliding_entity(self) -> bool:
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
           if self.is_colliding_entity:
            return True
        return False

    x = property(get_x, set_x)
    y = property(get_y, set_y)
    coordinates = property(get_coordinates)
    width = property(get_width)
    height = property(get_height)
    is_colliding_entity = property(get_is_colliding_entity)


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


class Monolith(Block):
    """An entity that shows you an inscription when interacted with.
    """

    def __init__(self, xPos: int, yPos: int, width: int, height: int):
        """Inits the Monolith class.
        """
        self.is_being_read = False
        self._hitbox_width_reduction = 10
        super().__init__(xPos, yPos, width, height)

    def check_for_read(self, player) -> bool:
        """Checks if the monolith is being read.
        """
        if super().is_colliding_with_entity(player) == True:
            return True
        return False


class Door(Block):
    """An entity that sends you to a different level on contact.
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
        if super().is_colliding_with_entity(player) is True:
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
        self._max_health = 10
        self._health = 10
        self.current_loot = None
        self._invincible = False
        self._score = 0

        # how long is the punch going to last for
        self._punch_timer = 0
        self._cur_punch = Movement.no_movement

        super().__init__(self.xPos, self.yPos, width, height, True, 2)
        self._hitbox_x_offset = 15
        self._hitbox_y_offset = 10
        self._hitbox_width_reduction = 35
        self._hitbox_height_reduction = 10

    def move(self, directions: list[Movement], entities: list[Entity],enemies) -> None:
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
                self._punch_timer = 60
                self._cur_punch = Movement.left_punch

            if direction == Movement.right_punch:
                self.facing = Movement.right_punch
                self._punch_timer = 60
                self._cur_punch = Movement.right_punch
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

        if 0 < self._punch_timer:
            self._punch_timer -= 1
            directions.append(self._cur_punch)
            self.facing = self._cur_punch


                
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

        entities_to_return,enemies,got_loot = self.calculate_collition_results(entities,enemies,directions)
        self.update_loot_stats()
        return entities_to_return,enemies,got_loot

    def calculate_collition_results(self, entities,enemies,directions):
        for i,entity in enumerate(entities):
            if isinstance(entity, Enemy) and (self.is_colliding_with_entity(entity)):
                # checking if the player is puching the enemey and removing the enemy 
                if (Movement.left_punch in directions) and (entity.x < self.x):
                    self._score += 1
                elif (Movement.right_punch in directions) and (self.x < entity.x):
                    self._score += 1

                #decreasing your lives if you hit an enemy
                elif not self._invincible:
                    self._health -= entity._damage

                enemies.remove(entity)
                entities.pop(i)
              
            elif isinstance(entity, Loot) and (self.is_colliding_with_entity(entity)):
                self._health += entity.power
                if self._health <= self._max_health:
                    self._health = self._max_health
                # making the loot disapear when you hit it
                entities.pop(i)
                return entities,enemies,True
                

            elif isinstance(entity, JumpLoot) and (self.is_colliding_with_entity(entity)):
                self.current_loot = entity
                # increasing the jump height because it hit the loot
                self._jump_height += entity.jump_increase
                # making the loot disapear when you hit it
                entities.pop(i)
                return entities,enemies,True

            elif isinstance(entity, InvincibilityLoot) and (self.is_colliding_with_entity(entity)):
                self.current_loot = entity
                self._invincible = True
                # making the loot disapear when you hit it
                entities.pop(i)
                return entities,enemies,True
            elif isinstance(entity, Loot) and (self.is_colliding_with_entity(entity)):
                self._health += entity.power
                entities.pop(i)
                return entities,enemies,True

        return entities,enemies,False


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

        if isinstance(self.current_loot,InvincibilityLoot):
            if self.current_loot.power_up_time <= 0:
                self._invincible = False
                self.current_loot = None
            self.current_loot.power_up_time -= 1

            

    def get_health(self):
        return self._health

    def get_invincibility(self):
        return self._invincible

    def get_score(self):
        return self._score
    
    score = property(get_score)
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
        self.screen_width = SCREEN_WIDTH
        self.player = player
        #self.distance_to_player = 0
        self.xPos = random.randint(0, SCREEN_WIDTH)
        self.yPos = 0

        self.facing = Movement.left
        super().__init__(self.xPos, self.yPos, width, height, True, 1)

    def get_dammage(self) -> int:
        return self._damage

    def move(self, frame_count, entities: list[Entity]):
        self.gravity(entities)

        #only from top, no moving upwards
        if frame_count % 30 == 0:
            direction = random.choice(["left", "right"])
            if direction == "left" and self.xPos >= 0:
                self.xPos -= self._speed
                self.facing = Movement.left
            elif direction == "right" and self.xPos < self.screen_width - self._width:
                self.xPos += self._speed
                self.facing = Movement.right
        
        # follow the player if they are within a certain distance
        elif self.distance_to_player() < 200:
            if self.player.xPos < self.xPos:
                self.xPos -= self._speed
            elif self.xPos < self.player.xPos :
                self.xPos += self._speed
            elif self.yPos < self.player.yPos:
                self.yPos += self._speed

    def distance_to_player(self):
        """Returns
            the absolute distance of this enemy to the player
            in integer form.
        """
        x_distance = (self.player.x-self.x)**2
        y_distance = (self.player.y-self.y)**2

        distance = (x_distance + y_distance)**0.5

        return int(abs(distance))

    damage = property(get_dammage)

class Loot(Entity):
    """the Loot class contains power ups that the player can gain once they colide with it.
        
    Atributes:
        power: the potency of the loot
    """
    def __init__(self,xPos: int, yPos: int, width: int, height: int,power=2):
        self._power = power
        super().__init__(xPos, yPos, width, height, True)
    def get_power(self):
        return self._power
    power = property(get_power)

class JumpLoot(Loot):
    """loot that makes you jump higher.
        
        Atributes:
            jump_increase: the amoun that your jump height increases when you get the loot
            power_up_time: the time period that your increased jump height remains in place
    """
    def __init__(self,xPos: int, yPos: int, width: int, height: int,power=2,jump_increase=10,time=1000):
        self._jump_increase = jump_increase
        self.power_up_time = time
        super().__init__(xPos, yPos, width, height,power=power)
    def get_jump_increase(self):
        return self._jump_increase
    jump_increase = property(get_jump_increase)
    #power_up_time= property(get_power_up_time)


class InvincibilityLoot(Loot):
    """loot that renders the player unable to be damaged by enemies for a particular period."""
    def __init__(self,xPos: int, yPos: int, width: int, height: int,power=2,time=1000):
        self.power_up_time = time
        super().__init__(xPos,yPos, width, height,power=power)
