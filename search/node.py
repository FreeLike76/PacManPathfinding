
from pygame.math import Vector2


class Node:
    def __init__(self, pos):
        # this node position in grid
        self.pos = pos
        # next nodes
        self.nextPos = {}
