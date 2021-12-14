from entities.entity import *
from search.searchAlgorithms import *


class Enemy(Entity):
    """Enemy class, inherited from Entity, defines enemies attributes"""

    def __init__(self, app, pos, color, e_type="random"):
        """Initialization"""
        Entity.__init__(self, app, pos, color)

        # enemy path
        self.e_type = e_type
        # possible directions
        self.pos_dirs = [pygame.math.Vector2(-1, 0),
                         pygame.math.Vector2(0, -1),
                         pygame.math.Vector2(1, 0),
                         pygame.math.Vector2(0, 1)]

        # path to player
        self.path_to_player = []

    def update_overload_movement(self):
        """Enemy autopilot movement changes"""
        if self.e_type == "chaser":
            # find path to player
            if len(self.path_to_player) == 0:
                self.path_to_player = A_star(self.app, self.grid_pos, self.app.player.grid_pos,
                                             _heuristic="Pow2",
                                             _greedy=False,
                                             _count_coin=False)
            # if path is found (not on the same cell, etc.)
            if len(self.path_to_player) > 0:
                # then move towards player
                self.stored_direction = self.path_to_player.pop(0)

        # if enemy-random
        elif self.e_type == "random":

            while True:
                next_dir = np.random.randint(0, 4)
                if self.app.can_move(self.grid_pos, self.pos_dirs[next_dir]):
                    self.stored_direction = self.pos_dirs[next_dir]
                    break

    def respawn(self, x, y):
        self.grid_pos = pygame.math.Vector2(x, y)

        self.pix_pos = pygame.math.Vector2(self.grid_pos * CELL_PIXEL_SIZE)
        self.pix_pos.x += CELL_PIXEL_SIZE // 2
        self.pix_pos.y += CELL_PIXEL_SIZE // 2

        self.direction = pygame.math.Vector2(0, 0)
        self.stored_direction = pygame.math.Vector2(0, 0)
