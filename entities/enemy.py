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
            # find path to player
            path_to_player = A_star(self.app, self.grid_pos, self.app.player.grid_pos,
                                    _heuristic="Pow2",
                                    _greedy=True,
                                    _count_coin=False)
            # if path is found (not on the same cell, etc.)
            if len(path_to_player) > 0:
                # then move towards player
                self.stored_direction = path_to_player.pop(0)
        # if enemy-random
        elif self.e_type == "random" and not self.app.can_move(self.grid_pos, self.direction)\
                or self.direction == pygame.math.Vector2(0, 0):
            # possible directions
            pos_dirs = [pygame.math.Vector2(-1, 0),
                        pygame.math.Vector2(0, -1),
                        pygame.math.Vector2(1, 0),
                        pygame.math.Vector2(0, 1)]
            while True:
                next_dir = np.random.randint(0, 4)
                if self.app.can_move(self.grid_pos, pos_dirs[next_dir]):
                    self.stored_direction = pos_dirs[next_dir]
                    break

    def respawn(self, x, y):
        self.grid_pos = pygame.math.Vector2(x, y)

        self.pix_pos = pygame.math.Vector2(self.grid_pos * CELL_PIXEL_SIZE)
        self.pix_pos.x += CELL_PIXEL_SIZE // 2
        self.pix_pos.y += CELL_PIXEL_SIZE // 2

        self.direction = pygame.math.Vector2(0, 0)
        self.stored_direction = pygame.math.Vector2(0, 0)
