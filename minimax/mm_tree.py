from minimax.mm_entity import MMEntity
from minimax.mm_state import MMState


class MMTree:
    def __init__(self, player, enemies):
        temp_player = MMEntity("P", player.grid_pos, player.direction)
        temp_enemies = []
        for enemy in enemies:
            temp_enemies.append(MMEntity(enemy.e_type, enemy.grid_pos, enemy.direction))