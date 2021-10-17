from entities.entity import *


class Player(Entity):
    """Player class, inherited from Entity, defines player attributes"""

    def __init__(self, app, pos, color, lives):
        """Initialization"""
        Entity.__init__(self, app, pos, color)

        # autopilot [0 - off, 1 - simple, 2 - nodes4, 3 - all coins]
        self.autopilot_type = 0
        self.autopilot_has_path = False
        self.autopilot_direction = []

        # other
        self.lives = lives

    def input_direction(self, new_direction):
        """Saves input locations to stored_direction and disables autopilot"""
        # direction update on player's input
        self.stored_direction = new_direction
        self.autopilot_type = 0
        self.autopilot_has_path = False

    def update_overload_movement(self):
        """Player autopilot movement changes"""
        # if autopilot is enabled
        if self.autopilot_type != 0:
            self.direction = pygame.math.Vector2(0, 0)
            self.stored_direction = pygame.math.Vector2(0, 0)

            # 1. No path + simple
            if not self.autopilot_has_path and self.autopilot_type == 1:
                # find path
                self.autopilot_direction = self.app.search(self.grid_pos, self.app.grid_pos_mouse)
                self.autopilot_has_path = True
            # 2. No path + 4-nods-task
            if not self.autopilot_has_path and self.autopilot_type == 2:
                self.autopilot_direction = self.app.search4(self.grid_pos)
                self.autopilot_has_path = True
            # 3. No path + all-coins-task
            if not self.autopilot_has_path and self.autopilot_type == 3:
                self.autopilot_direction = self.app.search_all(self.grid_pos)
                self.autopilot_has_path = True
            # follow the path
            if len(self.autopilot_direction) > 0:
                self.stored_direction = self.autopilot_direction.pop(0)
            # if destination is reached stop autopilot
            else:
                self.autopilot_type = 0
                self.autopilot_has_path = False
                self.stored_direction = pygame.math.Vector2(0, 0)
