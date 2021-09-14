import pygame


class Player:
    """Player class defines player attributes"""
    def __init__(self, app, pos, color, lives):
        """Player initialization"""
        # app
        self.app = app

        # autopilot
        self.autopilot = False
        self.autopilot_has_path = False
        self.autopilot_direction = []

        # coords
        self.grid_pos = pygame.math.Vector2(pos)
        self.pix_pos = pygame.math.Vector2(self.grid_pos * self.app.cell_pixel_size)
        self.pix_pos.x += self.app.cell_pixel_size // 2
        self.pix_pos.y += self.app.cell_pixel_size // 2
        self.direction = pygame.math.Vector2(0, 0)
        self.stored_direction = pygame.math.Vector2(0, 0)

        # other
        self.lives = lives
        self.high_score = 0
        self.cur_score = 0
        self.color = color

    def draw(self):
        """Drawing the player on map"""
        pygame.draw.circle(self.app.screen, self.color,
                           self.pix_pos,
                           int(self.app.cell_pixel_size * 0.4))

    def draw_grid(self):
        """Helper function for debugging: drawing player location on grid"""
        # grid for debugging
        pygame.draw.rect(self.app.screen, self.color,
                         pygame.Rect(self.grid_pos[0] * self.app.cell_pixel_size,
                                     self.grid_pos[1] * self.app.cell_pixel_size,
                                     self.app.cell_pixel_size, self.app.cell_pixel_size), 1)
        # drawing path
        if self.autopilot and self.autopilot_has_path:
            self._draw_path = pygame.math.Vector2(self.grid_pos)
            pygame.draw.line(self.app.screen, self.color,
                             self.pix_pos,
                             self.app.end_pos_from_mouse * self.app.cell_pixel_size
                             + pygame.math.Vector2(self.app.cell_pixel_size * 0.5,
                                                   self.app.cell_pixel_size * 0.5))

    def move(self, new_direction):
        """Saves input locations to stored_direction and disables autopilot"""
        # direction update on player's input
        self.stored_direction = new_direction
        self.autopilot = False
        self.autopilot_has_path = False

    def update(self):
        """Defines player movements after human input or during autopilot"""
        # if centered
        if self.pix_pos.x % self.app.cell_pixel_size == self.app.cell_pixel_size // 2 \
                and self.pix_pos.y % self.app.cell_pixel_size == self.app.cell_pixel_size // 2:
            # if autopilot is enabled
            if self.autopilot:
                self.direction = pygame.math.Vector2(0, 0)
                self.stored_direction = pygame.math.Vector2(0, 0)
                # if path was not found yet
                if not self.autopilot_has_path:
                    # find path
                    self.autopilot_direction = self.app.search(self.grid_pos, self.app.end_pos_from_mouse)
                    self.autopilot_has_path = True
                # follow the path
                if len(self.autopilot_direction) > 0:
                    self.stored_direction = self.autopilot_direction.pop(0)
                # if destination is reached stop autopilot
                else:
                    self.autopilot = False
                    self.autopilot_has_path = False
                    self.stored_direction = pygame.math.Vector2(0, 0)
            # if can change dir
            if self.app.can_move(self.grid_pos, self.stored_direction):
                self.direction = self.stored_direction
            # if can't move
            elif not self.app.can_move(self.grid_pos, self.direction):
                self.direction = pygame.math.Vector2(0, 0)

        # update grid position using pixel position (for smooth movements)
        self.pix_pos += self.direction
        self.grid_pos = self.pix_pos // self.app.cell_pixel_size
