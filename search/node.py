
from pygame.math import Vector2


class Node:
    """Saves current game position, used in search"""
    def __init__(self, pos, parent=None, cost=0):
        """Node initialization"""
        # this node position in grid
        self.pos = pos
        # next nodes
        self.nextPos = []
        # parent ref, used in bfs
        self.parent = parent
        # score for uni-cost
        self.cost = cost
        # coins map
        self.coins_map = None
