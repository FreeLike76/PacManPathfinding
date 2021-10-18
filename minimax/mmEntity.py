class MMEntity:
    def __init__(self, e_type, grid_pos, prev_direction=None):
        self.e_type = e_type
        self.grid_pos = grid_pos
        self.prev_direction = prev_direction
