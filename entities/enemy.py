from entities.entity import *
from search.searchAlgorithms import *


class Enemy(Entity):
    """Enemy class, inherited from Entity, defines enemies attributes"""

    def __init__(self, app, pos, color, e_type="random"):
        """Initialization"""
        Entity.__init__(self, app, pos, color)

        # enemy path
        self.e_type = e_type

    def update_overload_movement(self):
        """Enemy autopilot movement changes"""
        if self.e_type == "chaser":
            self.stored_direction = A_star(self.app, self.grid_pos, self.app.player.grid_pos,
                                           _heuristic="Pow2",
                                           _greedy=True,
                                           _count_coin=False).pop(0)

        elif self.e_type == "random" and self.direction == pygame.math.Vector2(0, 0):
            pos_dirs = [pygame.math.Vector2(-1, 0),
                        pygame.math.Vector2(0, -1),
                        pygame.math.Vector2(1, 0),
                        pygame.math.Vector2(0, 1)]
            while True:
                next_dir = np.random.randint(0, 4)
                if self.app.can_move(self.grid_pos, pos_dirs[next_dir]):
                    self.stored_direction = pos_dirs[next_dir]
                    break
