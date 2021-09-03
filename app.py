import pygame
import sys
from appSettings import *

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "start"

        self.load_images()
        self.high_score = 10
        self.cell_shape = (28, 31)

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
        # background black
        self.screen.fill(BLACK)
        # menu

        self.draw_text("PACMAN",
                       self.screen, [WIDTH_BACKGROUND // 2, HEIGHT // 2 - BIG_TEXT_SIZE * 2],
                       LOGO_TEXT_SIZE, MENU_ORANGE, DEFAULT_FONT, True, True)
        self.draw_text("Dmytro Geleshko",
                       self.screen, [WIDTH_BACKGROUND // 2, HEIGHT // 2],
                       SMALL_TEXT_SIZE, MENU_BLUE, DEFAULT_FONT, True, True)
        self.draw_text("IP-91",
                       self.screen, [WIDTH_BACKGROUND // 2, HEIGHT // 2 + SMALL_TEXT_SIZE],
                       SMALL_TEXT_SIZE, MENU_BLUE, DEFAULT_FONT, True, True)
        self.draw_text("PRESS SPACE TO PLAY",
                       self.screen, [WIDTH_BACKGROUND // 2, HEIGHT // 2 + BIG_TEXT_SIZE * 2 + SMALL_TEXT_SIZE],
                       BIG_TEXT_SIZE, MENU_ORANGE, DEFAULT_FONT, True, True)
        self.draw_info()
        pygame.display.update()

    # PLAY FUNCTIONS

    def play_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def play_update(self):
        pass

    def play_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.image_background, (0, 0))
        #self.draw_grid()
        self.draw_info()
        pygame.display.update()

    # SUPPORT FUNCTIONS

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
        for i in range(1, self.cell_shape[0]):
            pygame.draw.line(self.screen, GRAY,
                             (i * WIDTH_CELL, 0),
                             (i * WIDTH_CELL, HEIGHT_BACKGROUND))
        for i in range(1, self.cell_shape[1]):
            pygame.draw.line(self.screen, GRAY,
                             (0, i * HEIGHT_CELL),
                             (WIDTH_BACKGROUND, i * HEIGHT_CELL))

    def draw_info(self, shade=False):
        pygame.draw.line(self.screen, WHITE,
                         (WIDTH_BACKGROUND + 1, 0),
                         (WIDTH_BACKGROUND + 1, HEIGHT_BACKGROUND), 1)

        pygame.draw.line(self.screen, WHITE,
                         (WIDTH_BACKGROUND + 4, 0),
                         (WIDTH_BACKGROUND + 4, HEIGHT_BACKGROUND), 3)
        pygame.draw.line(self.screen, WHITE,
                         (WIDTH_BACKGROUND + 7, 0),
                         (WIDTH_BACKGROUND + 7, HEIGHT_BACKGROUND), 1)
        self.draw_text("HIGH SCORE",
                       self.screen,
                       [(WIDTH - WIDTH_BACKGROUND) // 2 + WIDTH_BACKGROUND, 0],
                       MID_TEXT_SIZE, WHITE, DEFAULT_FONT, True, False)
        self.draw_text(str(self.high_score),
                       self.screen,
                       [(WIDTH - WIDTH_BACKGROUND) // 2 + WIDTH_BACKGROUND, MID_TEXT_SIZE],
                       MID_TEXT_SIZE, WHITE, DEFAULT_FONT, True, False)
