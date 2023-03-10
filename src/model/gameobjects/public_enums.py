
import enum


class Movement(enum.Enum):
    right = 1
    left = 2
    jump = 3
    no_movement = 4
    left_punch = 5
    right_punch = 6

class GameState(enum.Enum):
    in_session = 1
    start_menu = 2
    leaderboard = 3
    about = 4
    help_screen = 5
    game_over = 6

class EnemySprite(enum.Enum):
    mummy_spritesheet = 1
    anubis_spritesheet = 2
    horus_spritesheet = 3
    sobek_spritesheet = 4
