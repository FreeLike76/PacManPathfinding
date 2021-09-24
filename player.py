import pygame
from appSettings import *


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
        self.pix_pos = pygame.math.Vector2(self.grid_pos * CELL_PIXEL_SIZE)
        self.pix_pos.x += CELL_PIXEL_SIZE // 2
        self.pix_pos.y += CELL_PIXEL_SIZE // 2
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
                           int(CELL_PIXEL_SIZE * 0.4))

    def draw_grid(self):
        """Helper function for debugging: drawing player location on grid"""
        # grid for debugging
        pygame.draw.rect(self.app.screen, self.color,
                         pygame.Rect(self.grid_pos[0] * CELL_PIXEL_SIZE,
                                     self.grid_pos[1] * CELL_PIXEL_SIZE,
                                     CELL_PIXEL_SIZE, CELL_PIXEL_SIZE), 1)
        # drawing path
        if self.autopilot and self.autopilot_has_path:
            pygame.draw.line(self.app.screen, RED,
                             self.pix_pos,
                             self.app.end_pos_from_mouse * CELL_PIXEL_SIZE
                             + pygame.math.Vector2(CELL_PIXEL_SIZE * 0.5,
                                                   CELL_PIXEL_SIZE * 0.5))

    def move(self, new_direction):
        """Saves input locations to stored_direction and disables autopilot"""
        # direction update on player's input
        self.stored_direction = new_direction
        self.autopilot = False
        self.autopilot_has_path = False

    def update(self):
        """Defines player movements after human input or during autopilot"""
        # if centered
        if self.pix_pos.x % CELL_PIXEL_SIZE == CELL_PIXEL_SIZE // 2 \
                and self.pix_pos.y % CELL_PIXEL_SIZE == CELL_PIXEL_SIZE // 2:
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
        self.grid_pos = self.pix_pos // CELL_PIXEL_SIZE
