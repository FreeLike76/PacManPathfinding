import pygame
from appSettings import *

class Entity:
    """Player class defines player attributes"""
    def __init__(self, app, pos, color):
        """Player initialization"""
        # app
        self.app = app

        # coordinates
        self.grid_pos = pygame.math.Vector2(pos)
        self.pix_pos = pygame.math.Vector2(self.grid_pos * CELL_PIXEL_SIZE)
        self.pix_pos.x += CELL_PIXEL_SIZE // 2
        self.pix_pos.y += CELL_PIXEL_SIZE // 2
        self.direction = pygame.math.Vector2(0, 0)
        self.stored_direction = pygame.math.Vector2(0, 0)

        # other
        self.color = color

    def draw(self):
        """Drawing .self on map"""
        pygame.draw.circle(self.app.screen, self.color,
                           self.pix_pos,
                           int(CELL_PIXEL_SIZE * 0.4))

    def draw_grid(self):
        """Helper function for debugging: drawing .self location on grid"""
        # grid for debugging
        pygame.draw.rect(self.app.screen, self.color,
                         pygame.Rect(self.grid_pos[0] * CELL_PIXEL_SIZE,
                                     self.grid_pos[1] * CELL_PIXEL_SIZE,
                                     CELL_PIXEL_SIZE, CELL_PIXEL_SIZE), 1)

    #def draw_path(self):
    #    # drawing path
    #    if self.autopilot_type == 1 and self.autopilot_has_path:
    #        pygame.draw.line(self.app.screen, RED,
    #                         self.pix_pos,
    #                         self.app.grid_pos_mouse * CELL_PIXEL_SIZE
    #                         + pygame.math.Vector2(CELL_PIXEL_SIZE * 0.5,
    #                                               CELL_PIXEL_SIZE * 0.5))

    def update_overload_movement(self):
        """Must be overloaded"""
        pass

    def update(self):
        """Defines player movements after human input or during autopilot"""
        # if centered
        if self.pix_pos.x % CELL_PIXEL_SIZE == CELL_PIXEL_SIZE // 2 \
                and self.pix_pos.y % CELL_PIXEL_SIZE == CELL_PIXEL_SIZE // 2:

            # overloaded movement
            self.update_overload_movement()

            # if can change dir
            if self.app.can_move(self.grid_pos, self.stored_direction):
                self.direction = self.stored_direction
            # if can't move
            elif not self.app.can_move(self.grid_pos, self.direction):
                self.direction = pygame.math.Vector2(0, 0)

        # update grid position using pixel position (for smooth movements)
        self.pix_pos += self.direction
        self.grid_pos = self.pix_pos // CELL_PIXEL_SIZE
