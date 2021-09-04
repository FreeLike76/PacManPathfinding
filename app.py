import pygame
import sys
from player import *
from appSettings import *
from map import grid

pygame.init()


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "start"

        self.load_images()
        self.grid_shape = (28, 31)
        self.cell_pixel_size = 20
        self.grid = [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]  # T

        self.player = Player(self, START_POS, PLAYER_COLOR)

    def run(self):
        while self.running:
            if self.state == "start":
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == "play":
                self.play_events()
                self.play_update()
                self.play_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    # START MENU FUNCTIONS

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = "play"

    def start_update(self):
        pass

    def start_draw(self):
        # fill background
        self.screen.fill(BLACK)

        # menu
        self.draw_text("PACMAN",
                       self.screen, [WIDTH_BACKGROUND // 2, HEIGHT // 2 - LOGO_TEXT_SIZE],
                       LOGO_TEXT_SIZE, MENU_ORANGE, DEFAULT_FONT, True, True)
        self.draw_text("Dmytro Geleshko",
                       self.screen, [WIDTH_BACKGROUND // 2, HEIGHT // 2 - SMALL_TEXT_SIZE],
                       SMALL_TEXT_SIZE, MENU_BLUE, DEFAULT_FONT, True, True)
        self.draw_text("IP-91",
                       self.screen, [WIDTH_BACKGROUND // 2, HEIGHT // 2],
                       SMALL_TEXT_SIZE, MENU_BLUE, DEFAULT_FONT, True, True)
        self.draw_text("PRESS SPACE TO PLAY",
                       self.screen, [WIDTH_BACKGROUND // 2, HEIGHT // 2 + BIG_TEXT_SIZE * 2],
                       BIG_TEXT_SIZE, MENU_ORANGE, DEFAULT_FONT, True, True)
        self.draw_info()
        pygame.display.update()

    # PLAY FUNCTIONS

    def play_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(pygame.math.Vector2(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(pygame.math.Vector2(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(pygame.math.Vector2(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(pygame.math.Vector2(0, 1))

    def play_update(self):
        self.player.update()

    def play_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.image_background, (0, 0))
        self.draw_grid()
        self.draw_info()
        self.player.draw()
        self.player.draw_grid()
        pygame.display.update()

    # SUPPORT FUNCTIONS

    def can_move(self, pos, direction):
        if self.grid[int(pos[0] + direction[0])][int(pos[1] + direction[1])] == 0:
            return False
        return True

    def load_images(self):
        self.image_background = pygame.image.load("images/background.png")

    def draw_text(self, text, screen, pos, size, color, font_name, make_centered_w=False, make_centered_h=False):
        # define font
        font = pygame.font.SysFont(font_name, size)
        # render font
        on_screen_text = font.render(text, False, color)
        # place at pos
        if make_centered_w:
            pos[0] = pos[0] - on_screen_text.get_size()[0] // 2
        if make_centered_h:
            pos[1] = pos[1] - on_screen_text.get_size()[1] // 2
        screen.blit(on_screen_text, pos)

    def draw_grid(self):
        for i in range(1, self.grid_shape[0]):
            pygame.draw.line(self.screen, GRAY,
                             (i * self.cell_pixel_size, 0),
                             (i * self.cell_pixel_size, HEIGHT_BACKGROUND))
        for i in range(1, self.grid_shape[1]):
            pygame.draw.line(self.screen, GRAY,
                             (0, i * self.cell_pixel_size),
                             (WIDTH_BACKGROUND, i * self.cell_pixel_size))
        for i in range(self.grid_shape[0]):
            for j in range(self.grid_shape[1]):
                if self.grid[i][j] == 0:
                    pygame.draw.rect(self.screen, RED,
                                     pygame.Rect(i * self.cell_pixel_size, j * self.cell_pixel_size,
                                                 self.cell_pixel_size, self.cell_pixel_size), 1)

    def draw_info(self):
        # screen split
        pygame.draw.line(self.screen, WHITE,
                         (WIDTH_BACKGROUND + 1, 0),
                         (WIDTH_BACKGROUND + 1, HEIGHT_BACKGROUND), 1)

        pygame.draw.line(self.screen, WHITE,
                         (WIDTH_BACKGROUND + 4, 0),
                         (WIDTH_BACKGROUND + 4, HEIGHT_BACKGROUND), 3)
        pygame.draw.line(self.screen, WHITE,
                         (WIDTH_BACKGROUND + 7, 0),
                         (WIDTH_BACKGROUND + 7, HEIGHT_BACKGROUND), 1)

        # high score
        self.draw_text("HIGH SCORE",
                       self.screen,
                       [(WIDTH - WIDTH_BACKGROUND) // 2 + WIDTH_BACKGROUND, 0],
                       MID_TEXT_SIZE, WHITE, DEFAULT_FONT, True, False)
        self.draw_text(str(self.player.high_score),
                       self.screen,
                       [(WIDTH - WIDTH_BACKGROUND) // 2 + WIDTH_BACKGROUND, MID_TEXT_SIZE],
                       MID_TEXT_SIZE, WHITE, DEFAULT_FONT, True, False)

        # cur score
        self.draw_text("CURRENT SCORE",
                       self.screen,
                       [(WIDTH - WIDTH_BACKGROUND) // 2 + WIDTH_BACKGROUND, MID_TEXT_SIZE * 3],
                       MID_TEXT_SIZE, WHITE, DEFAULT_FONT, True, False)
        self.draw_text(str(self.player.cur_score),
                       self.screen,
                       [(WIDTH - WIDTH_BACKGROUND) // 2 + WIDTH_BACKGROUND, MID_TEXT_SIZE * 4],
                       MID_TEXT_SIZE, WHITE, DEFAULT_FONT, True, False)

        # lives

        # type of search

        # time of search
