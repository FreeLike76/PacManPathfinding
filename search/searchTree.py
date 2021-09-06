from node import *
from pygame.math import Vector2


class SearchTree:
    def __init__(self, root_pos, end_pos):
        self.root = Node(root_pos)
        self.end_pos = end_pos
        # possible directions: left, right, up, down
        self.directions = [Vector2(-1, 0), Vector2(1, 0), Vector2(0, -1), Vector2(0, 1)]
        # best path
        self.path = []
