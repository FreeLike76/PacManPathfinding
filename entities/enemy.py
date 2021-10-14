from entities.entity import *


class Enemy(Entity):
    """Enemy class, inherited from Entity, defines enemies attributes"""

    def __init__(self, app, pos, color, type="random"):
        """Initialization"""
        Entity.__init__(self, app, pos, color)

        # enemy path
        self.autopilot_has_path = False
        self.autopilot_direction = []
        self.type = type

    def update_overload_movement(self):
        """Enemy autopilot movement changes"""
        if self.type == "chaser":
            if not self.autopilot_has_path:
                # find path
                self.autopilot_direction = self.app.search(self.grid_pos, self.app.player.grid_pos, False)
                self.autopilot_has_path = True
            # follow the path
            if len(self.autopilot_direction) > 0:
                self.stored_direction = self.autopilot_direction.pop(0)
            # if destination is reached stop autopilot
            else:
                self.autopilot_has_path = False
                self.stored_direction = pygame.math.Vector2(0, 0)
        else:
            self.stored_direction = pygame.math.Vector2(1, 0)
