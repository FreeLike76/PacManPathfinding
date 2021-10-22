from search.searchAlgorithms import *
from minimax.mmEntity import MMEntity
from minimax.mmState import MMState


class MMTree:
    def __init__(self, app, player, enemies, depth):
        # app reference
        self.app = app

        # setting up the tree depth
        self.tree_depth = (len(enemies) + 1) * depth

        # possible entity directions
        self.directions = [pygame.math.Vector2(-1, 0),
                           pygame.math.Vector2(0, -1),
                           pygame.math.Vector2(1, 0),
                           pygame.math.Vector2(0, 1)]

        # root
        start_root_entities = [MMEntity("player", player.grid_pos)]
        for enemy in enemies:
            start_root_entities.append(MMEntity(enemy.e_type, enemy.grid_pos, enemy.direction))
        self.root = MMState(start_root_entities, 0)

        # init tree
        self.build(self.root)

    def build(self, state, cur_depth=0):
        # IF REACHED THE BOTTOM
        if cur_depth == self.tree_depth:
            state.eval()
            return

        # IF NO CHILDREN
        if len(state.next_states) == 0:

            # IF PLAYER IS ACTIVE
            if state.entities[state.active_id].e_type == "player":
                self.add_states_player(state)

            # ELSE IF ENEMY-RANDOM IS ACTIVE
            elif state.entities[state.active_id].e_type == "random":
                # if enemy-random doesn't have direction
                # or has collided with the wall
                if state.entities[state.active_id].prev_direction == pygame.math.Vector2(0, 0) \
                        or not self.app.can_move(state.entities[state.active_id].grid_pos,
                                                 state.entities[state.active_id].prev_direction):
                    self.add_states_enemy_random_new_direction(state)
                # else same direction
                else:
                    self.add_states_enemy_random_old_direction(state)

            # IF ENEMY-CHASER IS ACTIVE
            elif state.entities[state.active_id].e_type == "chaser":
                self.add_states_enemy_chaser(state)

        # RECURRENT FOR ALL CHILD-STATES (and update active_id)
        for next_state in state.next_states:
            self.build(next_state, cur_depth + 1)

        # THEN UPDATE SCORE
        state.score = state.next_states[state.find_max_child_index()].score
        return

    def add_states_player(self, state):
        """Appends next_states to state-node, where player is considered active"""
        for _dir in self.directions:
            if self.app.can_move(state.entities[state.active_id].grid_pos, _dir):
                # append state and change player pos
                state.copy_add_next_state()
                state.next_states[-1].entities[state.active_id].grid_pos = state.entities[state.active_id].grid_pos \
                                                                           + _dir

    def add_states_enemy_random_new_direction(self, state):
        """Enemy-Random just spawned or is changing direction because of collision with the wall"""
        for _dir in self.directions:
            if self.app.can_move(state.entities[state.active_id].grid_pos, _dir):
                # if enemy-random can move in _dir append state and update prev_direction
                state.copy_add_next_state()
                state.next_states[-1].entities[state.active_id].grid_pos = state.entities[state.active_id].grid_pos \
                                                                           + _dir
                state.next_states[-1].entities[state.active_id].prev_direction = _dir

    def add_states_enemy_random_old_direction(self, state):
        """Enemy-Random continues moving"""
        state.copy_add_next_state()
        state.next_states[-1].entities[state.active_id].grid_pos = state.entities[state.active_id].grid_pos \
                                                                   + state.entities[state.active_id].prev_direction

    def add_states_enemy_chaser(self, state):
        # find where will he move using greedy algorithm
        path_to_player = A_star(self.app, state.entities[state.active_id].grid_pos, state.entities[0].grid_pos,
                                _heuristic="Pow2",
                                _greedy=True,
                                _count_coin=False)

        _dir = pygame.math.Vector2(0, 0)

        # if algorithm found path
        if len(path_to_player) > 0:
            _dir = path_to_player.pop(0)
        # if not, try continue moving
        elif self.app.can_move(state.entities[state.active_id].grid_pos,
                               state.entities[state.active_id].prev_direction):
            _dir = state.entities[state.active_id].prev_direction

        # copy state
        state.copy_add_next_state()

        # update the entity itself
        state.next_states[-1].entities[state.active_id].grid_pos = state.entities[state.active_id].grid_pos + _dir
        state.next_states[-1].entities[state.active_id].prev_direction = _dir

    def next_state_by_pos(self, pos):
        """Update the tree (root) by passing the position of the entity in the game"""
        for next_state in self.root.next_states:
            if next_state.entities[self.root.active_id].grid_pos == pos:
                self.root = next_state
                break

    def best_player_state(self):
        """Returns the direction, recommended for the player by algorithm"""
        best_successor_id = self.root.find_max_child_index()
        return self.root.next_states[best_successor_id].entities[0].grid_pos - self.root.entities[0].grid_pos
