from problem import SearchState, SearchProblem
from typing import List, Callable
from util import Stack, Queue, PriorityQueue


def bfs_dfs(problem, frontier):
    parent = {}
    explored = set()
    explored_states_count = 0
    frontier.push(problem.get_initial_state())
    parent[problem.get_initial_state()] = None
    explored.add(problem.get_initial_state())
    while not frontier.is_empty():
        cur = frontier.pop()
        if problem.is_goal_state(cur):
            p = cur
            path = []
            while p:
                path.append(p)
                p = parent[p]
            path.reverse()
            return path, explored_states_count
        for next_state in problem.get_neighbors(cur):
            state = next_state[0]
            if state not in explored:
                parent[state] = cur
                frontier.push(state)
                explored.add(state)
                explored_states_count += 1
                
    return [], explored_states_count
        

def ucs_astar(problem, frontier, heuristic):
    parent = {}
    cost = {}
    explored = set()
    explored_states_count = 0
    frontier.push(problem.get_initial_state(), 0 + heuristic(problem.get_initial_state()))
    parent[problem.get_initial_state()] = None
    cost[problem.get_initial_state()] = 0
    
    while not frontier.is_empty():
        cur = frontier.pop()
        explored.add(cur)
        explored_states_count += 1
        if problem.is_goal_state(cur):
            p = cur
            path = []
            while p:
                path.append(p)
                p = parent[p]
            path.reverse()
            return path, explored_states_count
        for next_state in problem.get_neighbors(cur):
            state = next_state[0]
            if state not in cost:
                parent[state] = cur
                cost[state] = cost[cur] + next_state[2]
                frontier.push(state, cost[state] + heuristic(state))
            else:
                if cost[state] > cost[cur] + next_state[2]:
                    parent[state] = cur
                    cost[state] = cost[cur] + next_state[2]
                    frontier.update(state, cost[state] + heuristic(state))

    return [], explored_states_count


def bfs(problem: SearchProblem) -> [List[SearchState], int]:
    """
    Returns the path from the initial state of the problem to a goal state.
    :param problem: a SearchProblem
    :return: List[SearchState] representing the path
    """
    return bfs_dfs(problem, Queue())


def dfs(problem: SearchProblem) -> [List[SearchState], int]:
    """
    Returns the path from the initial state of the problem to a goal state.
    :param problem: a SearchProblem
    :return: List[SearchState] representing the path
    """
    return bfs_dfs(problem, Stack())


def ucs(problem: SearchProblem) -> [List[SearchState], int]:
    """
    Returns the path from the initial state of the problem to a goal state.
    :param problem: a SearchProblem
    :return: List[SearchState] representing the path
    """
    zero_heuristic = lambda state : 0
    return ucs_astar(problem, PriorityQueue(), zero_heuristic)


def astar(problem: SearchProblem, heuristic: Callable[[SearchState], float]) -> [List[SearchState], int]:
    """
    Returns the path from the initial state of the problem to a goal state.
    :param problem: a SearchProblem
    :return: List[SearchState] representing the path
    """
    return ucs_astar(problem, PriorityQueue(), heuristic)