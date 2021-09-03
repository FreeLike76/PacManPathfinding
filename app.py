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
        self.draw_text("HIGH SCORE",
                       self.screen, [5, 0],
                       MID_TEXT_SIZE, WHITE, DEFAULT_FONT, False)
        self.draw_text("PACMAN",
                       self.screen, [WIDTH // 2, HEIGHT // 2 - BIG_TEXT_SIZE * 2],
                       LOGO_TEXT_SIZE, MENU_ORANGE, DEFAULT_FONT, True)
        self.draw_text("Dmytro Geleshko",
                       self.screen, [WIDTH // 2, HEIGHT // 2],
                       MID_TEXT_SIZE, MENU_BLUE, DEFAULT_FONT, True)
        self.draw_text("IP-91",
                       self.screen, [WIDTH // 2, HEIGHT // 2 + MID_TEXT_SIZE],
                       MID_TEXT_SIZE, MENU_BLUE, DEFAULT_FONT, True)
        self.draw_text("PRESS SPACE TO PLAY",
                       self.screen, [WIDTH // 2, HEIGHT // 2 + BIG_TEXT_SIZE * 2 + MID_TEXT_SIZE],
                       BIG_TEXT_SIZE, MENU_ORANGE, DEFAULT_FONT, True)
        pygame.display.update()

    # PLAY FUNCTIONS

    def play_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def play_update(self):
        pass

    def play_draw(self):
        self.screen.fill(WHITE)
        pygame.display.update()

    # SUPPORT FUNCTIONS

    def draw_text(self, text, screen, pos, size, color, font_name, make_centered=False):
        # define font
        font = pygame.font.SysFont(font_name, size)
        # render font
        on_screen_text = font.render(text, False, color)
        # place at pos
        if make_centered:
            pos[0] = pos[0] - on_screen_text.get_size()[0] // 2
            pos[1] = pos[1] - on_screen_text.get_size()[1] // 2
        screen.blit(on_screen_text, pos)
