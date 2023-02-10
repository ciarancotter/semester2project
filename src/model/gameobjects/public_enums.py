import enum
class Movement(enum.Enum):
  right = 1
  left = 2
  jump = 3
  no_movement = 4

class GameState(enum.Enum):
	in_session = 1
	start_menue = 2
	leaderboard = 3
	about = 4
	help_screen = 5