import pygame
import sys
import time
from search.searchTree import *
from player import *
from appSettings import *
from map import grid

pygame.init()


class App:
    """Game class"""
    def __init__(self):
        """Game initialization"""
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        # state
        self.running = True
        self.state = "start"

        # images
        self.load_images()

        # map
        self.grid_shape = (28, 31)
        self.cell_pixel_size = 20
        self.grid = [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]  # T
        self.coins = [[1 if grid[j][i] == 1 else 0 for j in range(len(grid))] for i in range(len(grid[0]))]  # Coins map

        # entities
        self.player = Player(self, START_POS, PLAYER_COLOR, PLAYER_LIVES)

        # autopilot search
        self.search_type = "bfs"
        self.search_time = 0
        self.end_pos_from_mouse = pygame.math.Vector2(0, 0)
        self._debug_draw_path = []

        # score
        with open("score.txt", "r") as scoreboard:
            for line in scoreboard:
                num = int(line.strip())
                if int(num) > self.player.high_score:
                    self.player.high_score = int(num)

        # cost
        self.coin_value = COIN_VALUE
        self.transition_cost = TRANSITION_COST

    def run(self):
        """Main game cycle"""
        while self.running:
            if self.state == "start":
                self.start_events()
                self.start_draw()
            elif self.state == "play":
                self.play_events()
                self.play_update()
                self.play_draw()
            elif self.state == "end":
                self.end_events()
                self.end_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        with open("score.txt", "a") as scoreboard:
            scoreboard.write(str(self.player.cur_score) + "\n")
        pygame.quit()
        sys.exit()

    # START MENU FUNCTIONS

    def start_events(self):
        """Managing events during start menu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = "play"

    def start_draw(self):
        """Drawing the start menu"""
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
        """Managing events that happen during the game itself"""
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
                if event.key == pygame.K_ESCAPE:
                    self.player.lives -= 1
                if event.key == pygame.K_s:
                    if self.search_type == "dfs":
                        self.search_type = "bfs"
                    elif self.search_type == "bfs":
                        self.search_type = "uni cost"
                    else:
                        self.search_type = "dfs"

            if event.type == pygame.MOUSEBUTTONUP:
                if self.get_end_pos_from_mouse():
                    self.player.autopilot = True
                    self.player.autopilot_has_path = False

    def play_update(self):
        """Updating game state"""
        if self.player.lives == 0:
            self.state = "end"
        else:
            self.on_coin()
            self.player.update()

    def play_draw(self):
        """Drawing the game"""
        self.screen.fill(BLACK)
        self.screen.blit(self.image_background, (0, 0))
        self.draw_coins()
        self.draw_info()
        self.player.draw()
        if DEBUG:
            self.draw_grid()
            self.player.draw_grid()
        pygame.display.update()

    # END FUNCTIONS

    def end_events(self):
        """Managing events during end screen"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT \
                    or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.running = False

    def end_draw(self):
        """Drawing the end screen"""
        self.screen.fill(BLACK)
        self.draw_text("YOU DIED",
                       self.screen, [WIDTH_BACKGROUND // 2, HEIGHT // 2 - LOGO_TEXT_SIZE],
                       LOGO_TEXT_SIZE, MENU_ORANGE, DEFAULT_FONT, True, True)
        self.draw_text("PRESS SPACE TO CLOSE",
                       self.screen, [WIDTH_BACKGROUND // 2, HEIGHT // 2 + BIG_TEXT_SIZE * 2],
                       BIG_TEXT_SIZE, MENU_ORANGE, DEFAULT_FONT, True, True)
        self.draw_info()
        pygame.display.update()

    # SUPPORT FUNCTIONS

    def can_move(self, pos, direction):
        """Checks whether it is possible to move from given position in given direction"""
        if self.grid[int(pos[0] + direction[0])][int(pos[1] + direction[1])] == 0:
            return False
        return True

    def draw_coins(self):
        """Draws coins on game map"""
        for i in range(self.grid_shape[0]):
            for j in range(self.grid_shape[1]):
                if self.coins[i][j] == 1:
                    pygame.draw.circle(self.screen, MENU_ORANGE,
                                       (i * self.cell_pixel_size + self.cell_pixel_size // 2,
                                        j * self.cell_pixel_size + self.cell_pixel_size // 2),
                                       self.cell_pixel_size // 5)

    def on_coin(self):
        if self.coins[int(self.player.grid_pos[0])][int(self.player.grid_pos[1])] == 1:
            self.coins[int(self.player.grid_pos[0])][int(self.player.grid_pos[1])] = 0
            self.player.cur_score += self.coin_value

    def load_images(self):
        """Loads all the images (currently only the background)"""
        self.image_background = pygame.image.load("images/background.png")

    def draw_text(self, text, screen, pos, size, color, font_name, make_centered_w=False, make_centered_h=False):
        """Helper function to draw text on screen"""
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
        """Helper function for debugging: draws map grid and player position on it"""
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
        if DEBUG and self.player.autopilot:
            for pos in self._debug_draw_path:
                pygame.draw.rect(self.screen, PLAYER_COLOR,
                                 pygame.Rect(pos[0] * self.cell_pixel_size,
                                             pos[1] * self.cell_pixel_size,
                                             self.cell_pixel_size, self.cell_pixel_size), 2)

    def draw_info(self):
        """Draws the information about game to the right of game map"""
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
        self.draw_text("LIVES",
                       self.screen,
                       [(WIDTH - WIDTH_BACKGROUND) // 2 + WIDTH_BACKGROUND, MID_TEXT_SIZE * 6],
                       MID_TEXT_SIZE, WHITE, DEFAULT_FONT, True, False)
        self.draw_text(str(self.player.lives),
                       self.screen,
                       [(WIDTH - WIDTH_BACKGROUND) // 2 + WIDTH_BACKGROUND, MID_TEXT_SIZE * 7],
                       MID_TEXT_SIZE, WHITE, DEFAULT_FONT, True, False)

        # type of search
        self.draw_text("SEARCH",
                       self.screen,
                       [(WIDTH - WIDTH_BACKGROUND) // 2 + WIDTH_BACKGROUND, MID_TEXT_SIZE * 9],
                       MID_TEXT_SIZE, WHITE, DEFAULT_FONT, True, False)
        self.draw_text(self.search_type,
                       self.screen,
                       [(WIDTH - WIDTH_BACKGROUND) // 2 + WIDTH_BACKGROUND, MID_TEXT_SIZE * 10],
                       MID_TEXT_SIZE, WHITE, DEFAULT_FONT, True, False)

        # time of search
        self.draw_text("SEARCH TIME",
                       self.screen,
                       [(WIDTH - WIDTH_BACKGROUND) // 2 + WIDTH_BACKGROUND, MID_TEXT_SIZE * 12],
                       MID_TEXT_SIZE, WHITE, DEFAULT_FONT, True, False)
        self.draw_text("{:.3f}ms".format(round(self.search_time*1000, 3)),
                       self.screen,
                       [(WIDTH - WIDTH_BACKGROUND) // 2 + WIDTH_BACKGROUND, MID_TEXT_SIZE * 13],
                       MID_TEXT_SIZE, WHITE, DEFAULT_FONT, True, False)

    def get_end_pos_from_mouse(self):
        """Finds mouse pos after mouse click for autopilot engagement"""
        x, y = pygame.mouse.get_pos()
        x = x // self.cell_pixel_size
        y = y // self.cell_pixel_size
        if self.grid[x][y] == 1:
            self.end_pos_from_mouse = pygame.math.Vector2(x, y)
            return True
        return False


    # SEARCH

    def search(self, start, end):
        """Search function that calls the selected algorithm"""
        time_start = time.time()

        path = []

        if self.search_type == "dfs":
            path = self.dfs(start, end)
        elif self.search_type == "bfs":
            path = self.bfs(start, end)
        else:
            path = self.uni_cost(start, end)

        time_end = time.time()
        self.search_time = time_end - time_start

        if DEBUG:
            print("Cost:", len(path))
            print("Path:", path)
            # drawing path in-game
            self._debug_draw_path = []
            pos = pygame.math.Vector2(self.player.grid_pos)
            for dir_ in path:
                pos = pos + dir_
                self._debug_draw_path.append(pos)
        return path

    def bfs(self, start, end):
        """BFS SEARCH"""
        tree = SearchTree(start, end)
        frontier = [tree.root]
        explored = []

        while len(frontier) > 0:
            cur = frontier.pop(0)
            explored.append(cur.pos)
            if cur.pos == tree.end_pos:
                # creating temp ref and exec backpropagation until root is found
                temp = cur
                while temp.parent is not None:
                    tree.path.append(temp.pos-temp.parent.pos)
                    temp = temp.parent
                break
            else:
                for direction in tree.directions:
                    # if can_move and not visited => start _dfs from new pos
                    if self.can_move(cur.pos, direction) \
                            and cur.pos + direction not in explored \
                            and not self._search_node_in_frontier(frontier, cur.pos + direction):
                        # add child
                        cur.nextPos.append(Node(cur.pos + direction))
                        # ref to parent
                        cur.nextPos[-1].parent = cur
                        # add to frontier
                        frontier.append(cur.nextPos[-1])
        # returning reverse because path was found from end to start
        tree.path.reverse()
        return tree.path

    def _search_node_in_frontier(self, frontier, pos):
        """SEARCH helper fucntion: finds position coords in array of Nodes"""
        for node in frontier:
            if node.pos == pos:
                return True
        return False

    def dfs(self, start, end):
        """DFS SEARCH Starter"""
        tree = SearchTree(start, end)
        self._dfs(tree, tree.root, [], [])
        return tree.path

    def _dfs(self, tree, cur, path_hist, node_hist):
        """Recursive dfs search"""
        # flag as visited
        node_hist.append(cur.pos)
        # if we are further from start_pos then shortest path => return
        if len(tree.path) != 0 and len(tree.path) <= len(path_hist):
            if DEBUG:
                print("dfs: pruned")
            return
        # if found end pos check whether the path is shorter.
        if cur.pos == tree.end_pos:
            if len(tree.path) == 0 or len(tree.path) > len(path_hist):
                tree.path = path_hist.copy()
                if DEBUG:
                    print("dfs: found path\n", tree.path)
        # else continue searching
        else:
            for direction in tree.directions:
                # if can_move and not visited => start _dfs from new pos
                if self.can_move(cur.pos, direction) and cur.pos + direction not in node_hist:
                    path_hist_copy = path_hist.copy()
                    path_hist_copy.append(direction)
                    node_hist_copy = node_hist.copy()
                    self._dfs(tree,
                              Node(cur.pos + direction),
                              path_hist_copy,
                              node_hist_copy)

    def uni_cost(self, start, end):
        """UNICOST SEARCH"""
        tree = SearchTree(start, end)
        frontier = [tree.root]
        explored = []

        while len(frontier) > 0:
            # less cost => first to open
            frontier.sort(key=lambda node: node.cost)
            cur = frontier.pop(0)
            explored.append(cur.pos)
            if cur.pos == tree.end_pos:
                # creating temp ref and exec backpropagation until root is found
                temp = cur
                while temp.parent is not None:
                    tree.path.append(temp.pos-temp.parent.pos)
                    temp = temp.parent
                break
            else:
                for direction in tree.directions:
                    # if can_move and not visited => start _dfs from new pos
                    if self.can_move(cur.pos, direction) \
                            and cur.pos + direction not in explored \
                            and not self._search_node_in_frontier(frontier, cur.pos + direction):
                        # add child
                        cur.nextPos.append(Node(cur.pos + direction, cost=cur.cost + self.transition_cost))
                        # add reward if coin present
                        if self.coins[int(cur.nextPos[-1].pos[0])][int(cur.nextPos[-1].pos[1])] == 1:
                            cur.nextPos[-1].cost -= self.coin_value
                        # ref to parent
                        cur.nextPos[-1].parent = cur
                        # add to frontier
                        frontier.append(cur.nextPos[-1])
        # returning reverse because path was found from end to start
        tree.path.reverse()
        return tree.path
