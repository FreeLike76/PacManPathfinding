import pygame
from search.node import *


class SearchTree:
    """Class for building the search tree"""
    def __init__(self, root_pos, end_pos):
        self.root = Node(root_pos)
        self.end_pos = end_pos
        # possible directions: left, up, right, down
        self.directions = [pygame.math.Vector2(-1, 0), pygame.math.Vector2(0, -1), pygame.math.Vector2(1, 0), pygame.math.Vector2(0, 1)]
        # best path
        self.path = []
