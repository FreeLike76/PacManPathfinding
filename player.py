import pygame


class Player:
    def __init__(self, app, pos, color):
        # app
        self.app = app

        # coords
        self.grid_pos = pygame.math.Vector2(pos)
        self.pix_pos = pygame.math.Vector2(self.grid_pos * self.app.cell_pixel_size)
        self.pix_pos.x += self.app.cell_pixel_size // 2
        self.pix_pos.y += self.app.cell_pixel_size // 2
        self.direction = pygame.math.Vector2(1, 0)

        # other
        self.high_score = 0
        self.cur_score = 0
        self.color = color

    def draw(self):
        pygame.draw.circle(self.app.screen, self.color,
                           self.pix_pos,
                           self.app.cell_pixel_size // 2)

    def draw_grid(self):
        # grid for debugging
        pygame.draw.rect(self.app.screen, self.color,
                         pygame.Rect(self.grid_pos[0] * self.app.cell_pixel_size,
                                     self.grid_pos[1] * self.app.cell_pixel_size,
                                     self.app.cell_pixel_size, self.app.cell_pixel_size), 1)

    def move(self, new_direction):
        # direction update on player's input
        self.direction = new_direction

    def update(self):
        # update grid position using pixel position (for smooth movements)
        self.pix_pos += self.direction
        self.grid_pos = self.pix_pos // self.app.cell_pixel_size
