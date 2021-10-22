import search.heuristic as heuristic
import copy


class MMState:
    def __init__(self, entities, active_id):
        self.entities = entities

        if active_id == len(entities):
            self.active_id = 0
        else:
            self.active_id = active_id

        self.next_states = []
        self.score = 0

    def eval(self):
        """Evaluate state"""
        for i in range(1, len(self.entities)):
            self.score += min(10, heuristic.manhattan(self.entities[0].grid_pos, self.entities[i].grid_pos))

    def find_max_child_index(self):
        """Cycle through next_states and find index of one with best score"""
        best_state_i = 0
        for i in range(1, len(self.next_states)):
            if self.next_states[i].score > self.next_states[best_state_i].score:
                best_state_i = i
        return best_state_i

    def copy_add_next_state(self):
        self.next_states.append(MMState(copy.deepcopy(self.entities), self.active_id + 1))