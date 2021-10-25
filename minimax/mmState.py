import search.heuristic as heuristic
import copy
from appSettings import *


class MMState:
    def __init__(self, tree, entities, active_id):
        self.tree = tree
        self.entities = entities

        if active_id == len(entities):
            self.active_id = 0
        else:
            self.active_id = active_id

        self.next_states = []
        self.score = 0

    def eval(self):
        """Evaluate state"""
        # if terminal
        if len(self.next_states) == 0:
            self.score = 0
            for i in range(1, len(self.entities)):
                self.score += min(MINIMAX_MAX_ENEMY_DIST_SCORE,
                                  heuristic.pow_dist(self.entities[0].grid_pos, self.entities[i].grid_pos))
        else:
            # if enemy-random is active -> expectimax
            if self.entities[self.active_id].e_type == "random":
                for next_state in self.next_states:
                    self.score = next_state.score / len(self.next_states)
            # else passing highest score
            else:
                self.score = self.next_states[self.find_max_child_index()].score

            # but if parent state correspond to player move or there are no enemies (so just player is on the map)
            # and player is on coin -> +score
            if (len(self.entities) == 1 or self.active_id == 1) \
                    and self.tree.app.map.coins[int(self.entities[0].grid_pos[0]),
                                                int(self.entities[0].grid_pos[1])] == 1:
                self.score += MINIMAX_COIN_VALUE

    def find_max_child_index(self):
        """Cycle through next_states and find index of one with best score"""
        best_state_i = 0
        for i in range(1, len(self.next_states)):
            if self.next_states[i].score > self.next_states[best_state_i].score:
                best_state_i = i
        return best_state_i

    def copy_add_next_state(self):
        self.next_states.append(MMState(self.tree, copy.deepcopy(self.entities), self.active_id + 1))
