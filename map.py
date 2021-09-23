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

    def _random_split(self, x, y, min_room_size=9):
        """Adds vertical and horizontal walls until reaches min_room_size"""

        if abs(x[0] - x[1]) <= min_room_size or abs(y[0] - y[1]) <= min_room_size:
            return
        else:
            # random walls
            x_wall_pos = np.random.randint(x[0] + 1, x[1] - 1)
            y_wall_pos = np.random.randint(y[0] + 1, y[1] - 1)

            # x-wall doors
            x_wall_door_y0 = np.random.randint(y[0], y_wall_pos)
            x_wall_door_y1 = np.random.randint(y_wall_pos, y[1])

            # y-wall doors
            y_wall_door_x0 = np.random.randint(x[0], x_wall_pos)
            y_wall_door_x1 = np.random.randint(x_wall_pos, x[1])

            # walls
            self.walls[x_wall_pos, ::] = 1
            self.walls[::, y_wall_pos] = 1

            # x-doors
            self.walls[x_wall_pos, x_wall_door_y0] = 0
            self.walls[x_wall_pos, x_wall_door_y1] = 0

            # y-doors
            self.walls[y_wall_door_x0, y_wall_pos] = 0
            self.walls[y_wall_door_x1, y_wall_pos] = 0

            self._random_split(x=(x[0], x_wall_pos), y=(y[0], y_wall_pos))
            self._random_split(x=(x_wall_pos, x[1]), y=(y[0], y_wall_pos))
            self._random_split(x=(x[0], x_wall_pos), y=(y_wall_pos, y[1]))
            self._random_split(x=(x_wall_pos, x[1]), y=(y_wall_pos, y[1]))
