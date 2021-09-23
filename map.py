import numpy as np


class Map:
    def __init__(self):
        # if using std map
        self.shape = (32, 32)
        self.walls = np.zeros(self.shape)
        self._apply_border()
        self._random_split(x=(0, 31), y=(0, 31))
        self.coins = self.walls == 0

    def _random_map(self):
        pass

    def _apply_border(self):
        self.walls[0, ::] = 1
        self.walls[-1, ::] = 1
        self.walls[::, 0] = 1
        self.walls[::, -1] = 1

    def _random_split(self, x, y, min_room_size=2):
        """Adds vertical and horizontal walls until reaches min_room_size"""

        if abs(x[0] - x[1]) <= min_room_size or abs(y[0] - y[1]) <= min_room_size:
            return
        else:
            # random walls
            x_wall_pos = np.random.randint(x[0] + 1, x[1] - 1)
            y_wall_pos = np.random.randint(y[0] + 1, y[1] - 1)

            # walls
            self.walls[x_wall_pos, y[0]+2:y[1]-2] = 1
            self.walls[x[0]+2:x[1]-2, y_wall_pos] = 1

            self._random_split(x=(x[0], x_wall_pos), y=(y[0], y_wall_pos))
            self._random_split(x=(x_wall_pos, x[1]), y=(y[0], y_wall_pos))
            self._random_split(x=(x[0], x_wall_pos), y=(y_wall_pos, y[1]))
            self._random_split(x=(x_wall_pos, x[1]), y=(y_wall_pos, y[1]))
