from minimax.mm_entity import MMEntity
from minimax.mm_state import MMState

class MMTree:
    def __init__(self, player, enemies):
        temp_player = MMEntity("P", player.grid_pos, player.direction)
        temp_enemies = []
        for enemy in enemies:
            if enemy.e_type == "chaser":
                temp_enemies.append(MMEntity("Chaser", ))
            else:
                temp_enemies.append(MMEntity(enemy.grid_pos, ))