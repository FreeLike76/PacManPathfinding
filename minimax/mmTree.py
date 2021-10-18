import pygame
import copy
from search.searchAlgorithms import *
from minimax.mmEntity import MMEntity
from minimax.mmState import MMState


class MMTree:
    def __init__(self, app, player, enemies, depth):
        self.app = app
        self.tree_depth = (len(enemies) + 1) * depth
        self.directions = [pygame.math.Vector2(-1, 0),
                           pygame.math.Vector2(0, -1),
                           pygame.math.Vector2(1, 0),
                           pygame.math.Vector2(0, 1)]
        # root
        start_root_entities = [MMEntity("player", player.grid_pos)]
        for enemy in enemies:
            start_root_entities.append(MMEntity(enemy.e_type, enemy.grid_pos, enemy.direction))
        self.root = MMState(start_root_entities, 0)
        self.build(self.root, 0)

    def build(self, state, cur_depth):

        # ENTITY ACTIVITY CYCLE

        if state.active_id == len(state.entities):
            state.active_id = 0

        # IF REACHED THE BOTTOM

        if cur_depth == self.tree_depth:
            return self.eval(state)

        # IF NO CHILDREN

        if len(state.next_states) == 0:

            # IF PLAYER IS ACTIVE

            if state.entities[state.active_id].e_type == "player":
                # for all directions, you can move to
                for _dir in self.directions:
                    if self.app.can_move(state.entities[state.active_id].grid_pos, _dir):
                        # append state and change player pos
                        state.next_states.append(copy.deepcopy(state))
                        state.next_states[-1].entities[state.active_id].grid_pos = state.entities[state.active_id] \
                                                                                       .grid_pos + _dir

            # IF ENEMY-RANDOM IS ACTIVE

            elif state.entities[state.active_id].e_type == "random":
                # if he can continue movement in prev direction:
                if self.app.can_move(state.entities[state.active_id].grid_pos,
                                     state.entities[state.active_id].prev_direction):
                    state.next_states.append(copy.deepcopy(state))
                    state.next_states[-1].entities[state.active_id].grid_pos = state.entities[state.active_id] \
                                                                                   .grid_pos \
                                                                               + state.entities[state.active_id] \
                                                                                   .prev_direction
                else:
                    for _dir in self.directions:
                        if self.app.can_move(state.entities[state.active_id].grid_pos, _dir):
                            # append state and change player pos
                            state.next_states.append(copy.deepcopy(state))
                            state.next_states[-1].entities[state.active_id].grid_pos = state[state.active_id].grid_pos \
                                                                                       + _dir
                            state.next_states[-1].entities[state.active_id].prev_direction = _dir

            # IF ENEMY-CHASER IS ACTIVE

            elif state.entities[state.active_id].e_type == "chaser":
                # copy state
                state.next_states.append(copy.deepcopy(state))
                # find where will he move using greedy algorithm
                path_to_player = A_star(self.app, state.entities[state.active_id].grid_pos, state.entities[0].grid_pos,
                                        _heuristic="Pow2",
                                        _greedy=True,
                                        _count_coin=False)
                # if algorithm found path
                if len(path_to_player) > 0:
                    _dir = path_to_player.pop(0)
                # if not, try continue moving
                else:
                    _dir = state.entities[state.active_id].prev_direction
                # BUT if he cant move in that direction -> stop
                if not self.app.can_move(state.entities[state.active_id].grid_pos,
                                         state.entities[state.active_id].prev_direction):
                    _dir[0] = _dir[0] * 0
                    _dir[1] = _dir[1] * 0

                # update the entity itself
                state.next_states[-1].entities[state.active_id].grid_pos = state.entities[state.active_id] \
                                                                               .grid_pos \
                                                                           + _dir
                state.next_states[-1].entities[state.active_id].prev_direction = _dir

        # REC FOR ALL CHILD-STATES (and update active_id)
        for next_state in state.next_states:
            next_state.active_id += 1
            self.build(next_state, cur_depth + 1)

    def eval(self, state):
        return 1
