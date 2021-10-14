from entities.entity import *


class Enemy(Entity):
    """Enemy class, inherited from Entity, defines enemies attributes"""

    def __init__(self, app, pos, color):
        """Player initialization"""
        Entity.__init__(self, app, pos, color)