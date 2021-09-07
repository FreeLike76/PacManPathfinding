
from pygame.math import Vector2


class Node:
    def __init__(self, pos, parent=None, cost=0):
        # this node position in grid
        self.pos = pos
        # next nodes
        self.nextPos = []
        # parent ref, used in bfs
        self.parent = parent
        # score for uni-cost
        self.cost = cost
