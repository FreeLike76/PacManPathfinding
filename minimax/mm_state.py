import pygame
from minimax.mm_entity import MMEntity
from appSettings import *


class MMState:
    def __init__(self, player, enemies):
        self.player_pos = player
        self.enemies = enemies
