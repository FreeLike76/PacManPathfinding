import pygame
from minimax.mmEntity import MMEntity
from appSettings import *


class MMState:
    def __init__(self, entities, active_id):
        self.entities = entities
        self.active_id = active_id
        self.nextStates = []
