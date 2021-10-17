from entities.entity import *
from search.searchAlgorithms import *


class Enemy(Entity):
    """Enemy class, inherited from Entity, defines enemies attributes"""

    def __init__(self, app, pos, color, type="random"):
        """Initialization"""
        Entity.__init__(self, app, pos, color)

        # enemy path
        self.type = type

    def update_overload_movement(self):
        """Enemy autopilot movement changes"""
        if self.type == "chaser":
            self.stored_direction = A_star(self.app, self.grid_pos, self.app.player.grid_pos,
                                           _heuristic="Pow2",
                                           _greedy=True,
                                           _count_coin=False).pop(0)

        else:
            self.stored_direction = pygame.math.Vector2(1, 0)
