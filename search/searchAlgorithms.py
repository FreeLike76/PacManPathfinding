import numpy as np
from search import heuristic
from search.searchTree import *
from appSettings import *


def A_star(app, start, end, _heuristic="Manhattan", _greedy=False, _count_coin=False):
    """A* search with different heuristics and greedy variant"""
    tree = SearchTree(start, end)
    frontier = [tree.root]
    explored = []

    while len(frontier) > 0:
        # less cost => first to open
        frontier.sort(key=lambda node: node.cost)
        cur = frontier.pop(0)
        explored.append(cur.pos)
        if cur.pos == tree.end_pos:
            # creating temp ref and exec backpropagation until root is found
            temp = cur
            while temp.parent is not None:
                tree.path.append(temp.pos - temp.parent.pos)
                temp = temp.parent
            break
        else:
            for direction in tree.directions:
                # if can_move and not visited => start _dfs from new pos
                if app.can_move(cur.pos, direction) \
                        and cur.pos + direction not in explored \
                        and not _search_node_in_frontier(frontier, cur.pos + direction):

                    # calculate heuristic
                    if _heuristic == "Euclidean":
                        cost = heuristic.euclidean(cur.pos + direction, tree.end_pos) * HEURISTIC_WEIGHT
                    elif _heuristic == "Pow2":
                        cost = heuristic.pow_dist(cur.pos + direction, tree.end_pos) * HEURISTIC_WEIGHT
                    else:
                        cost = heuristic.manhattan(cur.pos + direction, tree.end_pos) * HEURISTIC_WEIGHT

                    # if not greedy + hist_cost and transition_cost
                    if not _greedy:
                        cost += (cur.cost + app.transition_cost)

                    # add reward if coin present
                    if _count_coin and \
                            app.map.coins[int((cur.pos + direction)[0])][int((cur.pos + direction)[1])] == 1:
                        cost -= COIN_VALUE

                    # add child
                    cur.nextPos.append(Node(cur.pos + direction, cost=cost))

                    # ref to parent
                    cur.nextPos[-1].parent = cur

                    # add to frontier
                    frontier.append(cur.nextPos[-1])

    # returning reverse because path was found from end to start
    tree.path.reverse()
    return tree.path

# Was optimal search all coins algorithm but toooo slow
"""def uni_cost_all_coins(app, start):
    tree = SearchTree(start, None)
    frontier = [tree.root]
    #explored = []

    tree.root.coins_map = app.map.coins.copy()

    while len(frontier) > 0:
        # less cost => first to open
        frontier.sort(key=lambda node: node.cost)
        cur = frontier.pop(0)
        #explored.append(cur.pos)
        print(cur.pos)
        if cur.coins_map.sum() == 0:
            # creating temp ref and exec backpropagation until root is found
            temp = cur
            while temp.parent is not None:
                tree.path.append(temp.pos - temp.parent.pos)
                temp = temp.parent
            break
        else:
            for direction in tree.directions:
                # if can_move and not visited => start _dfs from new pos
                if app.can_move(cur.pos, direction) \
                        and not _search_node_in_frontier(frontier, cur.pos + direction):
                    # add child
                    cur.nextPos.append(Node(cur.pos + direction, cost=cur.cost + app.transition_cost))
                    # copy map
                    cur.nextPos[-1].coins_map = cur.coins_map.copy()
                    # add reward if coin present and remove coin on child's map
                    if cur.coins_map[int(cur.nextPos[-1].pos[0])][int(cur.nextPos[-1].pos[1])] == 1:
                        cur.nextPos[-1].cost -= COIN_VALUE
                        cur.nextPos[-1].coins_map[int(cur.nextPos[-1].pos[0])][int(cur.nextPos[-1].pos[1])] = 0
                    # ref to parent
                    cur.nextPos[-1].parent = cur
                    # add to frontier
                    frontier.append(cur.nextPos[-1])
    # returning reverse because path was found from end to start
    tree.path.reverse()
    return tree.path"""


def bfs(app, start, end):
    """BFS SEARCH"""
    tree = SearchTree(start, end)
    frontier = [tree.root]
    explored = []

    while len(frontier) > 0:
        cur = frontier.pop(0)
        explored.append(cur.pos)
        if cur.pos == tree.end_pos:
            # creating temp ref and exec backpropagation until root is found
            temp = cur
            while temp.parent is not None:
                tree.path.append(temp.pos - temp.parent.pos)
                temp = temp.parent
            break
        else:
            for direction in tree.directions:
                # if can_move and not visited => start _dfs from new pos
                if app.can_move(cur.pos, direction) \
                        and cur.pos + direction not in explored \
                        and not _search_node_in_frontier(frontier, cur.pos + direction):
                    # add child
                    cur.nextPos.append(Node(cur.pos + direction))
                    # ref to parent
                    cur.nextPos[-1].parent = cur
                    # add to frontier
                    frontier.append(cur.nextPos[-1])
    # returning reverse because path was found from end to start
    tree.path.reverse()
    return tree.path


def _search_node_in_frontier(frontier, pos):
    """SEARCH helper fucntion: finds position coords in array of Nodes"""
    for node in frontier:
        if node.pos == pos:
            return True
    return False


def dfs_full(app, start, end):
    """DFS SEARCH FULL+MOD"""
    tree = SearchTree(start, end)
    _dfs_full(app, tree, tree.root, [], [])
    return tree.path


def _dfs_full(app, tree, cur, path_hist, node_hist):
    """Recursive dfs search, FULL+MOD"""
    # flag as visited
    node_hist.append(cur.pos)
    # if we are further from start_pos then shortest path => return
    if len(tree.path) != 0 and len(tree.path) <= len(path_hist):
        if DEBUG:
            print("dfs: pruned")
        return
    # if found end pos check whether the path is shorter.
    if cur.pos == tree.end_pos:
        if len(tree.path) == 0 or len(tree.path) > len(path_hist):
            tree.path = path_hist.copy()
            if DEBUG:
                print("dfs: found path\n", tree.path)
    # else continue searching
    else:
        for direction in tree.directions:
            # if can_move and not visited => start _dfs from new pos
            if app.can_move(cur.pos, direction) and cur.pos + direction not in node_hist:
                path_hist_copy = path_hist.copy()
                path_hist_copy.append(direction)
                node_hist_copy = node_hist.copy()
                _dfs_full(app,
                          tree,
                          Node(cur.pos + direction),
                          path_hist_copy,
                          node_hist_copy)


def uni_cost(app, start, end):
    """UNICOST SEARCH"""
    tree = SearchTree(start, end)
    frontier = [tree.root]
    explored = []

    while len(frontier) > 0:
        # less cost => first to open
        frontier.sort(key=lambda node: node.cost)
        cur = frontier.pop(0)
        explored.append(cur.pos)
        if cur.pos == tree.end_pos:
            # creating temp ref and exec backpropagation until root is found
            temp = cur
            while temp.parent is not None:
                tree.path.append(temp.pos - temp.parent.pos)
                temp = temp.parent
            break
        else:
            for direction in tree.directions:
                # if can_move and not visited => start _dfs from new pos
                if app.can_move(cur.pos, direction) \
                        and cur.pos + direction not in explored \
                        and not _search_node_in_frontier(frontier, cur.pos + direction):
                    # add child
                    cur.nextPos.append(Node(cur.pos + direction, cost=cur.cost + app.transition_cost))
                    # add reward if coin present
                    if app.map.coins[int(cur.nextPos[-1].pos[0])][int(cur.nextPos[-1].pos[1])] == 1:
                        cur.nextPos[-1].cost -= COIN_VALUE
                    # ref to parent
                    cur.nextPos[-1].parent = cur
                    # add to frontier
                    frontier.append(cur.nextPos[-1])
    # returning reverse because path was found from end to start
    tree.path.reverse()
    return tree.path


def dfs(app, start, end):
    """DFS SEARCH"""
    tree = SearchTree(start, end)
    _dfs(app, tree, tree.root, [], [])
    return tree.path


def _dfs(app, tree, cur, path_hist, node_hist):
    """Recursive dfs search"""
    # flag as visited
    node_hist.append(cur.pos)
    # if found end pos check whether the path is shorter.
    if cur.pos == tree.end_pos:
        tree.path = path_hist.copy()
    # else continue searching
    else:
        for direction in tree.directions:
            # if path not found and can_move and not visited => start _dfs from new pos
            if app.can_move(cur.pos, direction) and cur.pos + direction not in node_hist \
                    and len(tree.path) == 0:
                path_hist_copy = path_hist.copy()
                path_hist_copy.append(direction)
                #node_hist_copy = node_hist.copy()
                _dfs(app,
                     tree,
                     Node(cur.pos + direction),
                     path_hist_copy,
                     node_hist)
