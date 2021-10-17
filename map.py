import numpy as np
from appSettings import *


class Map:
    def __init__(self):
        self.shape = (32, 32)

        # add walls
        self.walls = np.zeros(self.shape)
        self._apply_border()
        self._random_split(x=(0, 31), y=(0, 31))

        # add coins
        self.coins = np.random.uniform(0, 1, self.shape)
        self.coins = self.coins < COIN_SPAWN_P
        self.coins[self.walls == 1] = False
        # to get unbiased score of player's performance during game
        self.coins_spawned = self.coins.sum()

    def _apply_border(self):
        self.walls[0, ::] = 1
        self.walls[-1, ::] = 1
        self.walls[::, 0] = 1
        self.walls[::, -1] = 1

    def _random_split(self, x, y, cross_doors=False, cross_doors_rand=False):
        """Adds vertical and horizontal walls until reaches min_room_size"""

        if abs(x[0] - x[1]) <= 3 or abs(y[0] - y[1]) <= 3:
            return
        else:
            # random walls (+2, -2) so that the walls are 1 block wide,
            # but randint is [min, max) => (+2, -1)
            x_wall_pos = np.random.randint(x[0] + 2, x[1] - 1)
            y_wall_pos = np.random.randint(y[0] + 2, y[1] - 1)

            # both walls, same here (+2, -1)
            self.walls[x_wall_pos, y[0] + 2: y[1] - 1] = 1
            self.walls[x[0] + 2: x[1] - 1, y_wall_pos] = 1

            # creating passages in the middle of cross-wall
            if cross_doors:
                if not cross_doors_rand:
                    self.walls[x_wall_pos + 1, y_wall_pos] = 0
                    self.walls[x_wall_pos - 1, y_wall_pos] = 0
                    self.walls[x_wall_pos, y_wall_pos + 1] = 0
                    self.walls[x_wall_pos, y_wall_pos - 1] = 0

                elif np.random.randn() > 0:
                    self.walls[x_wall_pos + 1, y_wall_pos] = 0
                    self.walls[x_wall_pos - 1, y_wall_pos] = 0

                else:
                    self.walls[x_wall_pos, y_wall_pos + 1] = 0
                    self.walls[x_wall_pos, y_wall_pos - 1] = 0

            # recursive call
            self._random_split(x=(x[0], x_wall_pos), y=(y[0], y_wall_pos))
            self._random_split(x=(x_wall_pos, x[1]), y=(y[0], y_wall_pos))
            self._random_split(x=(x[0], x_wall_pos), y=(y_wall_pos, y[1]))
            self._random_split(x=(x_wall_pos, x[1]), y=(y_wall_pos, y[1]))
