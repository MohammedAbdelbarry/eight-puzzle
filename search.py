from problem import SearchState, SearchProblem
from typing import List, Callable
from util import Stack, Queue, PriorityQueue


def bfs(problem: SearchProblem) -> List[SearchState]:
    """
    Returns the path from the initial state of the problem to a goal state.
    :param problem: a SearchProblem
    :return: List[SearchState] representing the path
    """
    return bfs_dfs(problem, Queue())


def dfs(problem: SearchProblem) -> List[SearchState]:
    """
    Returns the path from the initial state of the problem to a goal state.
    :param problem: a SearchProblem
    :return: List[SearchState] representing the path
    """
    return bfs_dfs(problem, Stack())


def ucs(problem: SearchProblem) -> List[SearchState]:
    """
    Returns the path from the initial state of the problem to a goal state.
    :param problem: a SearchProblem
    :return: List[SearchState] representing the path
    """
    raise NotImplementedError


def astar(problem: SearchProblem, h: Callable[[SearchState], [float]]=None) -> List[SearchState]:
    """
    Returns the path from the initial state of the problem to a goal state.
    :param problem: a SearchProblem
    :return: List[SearchState] representing the path
    """
    raise NotImplementedError

def bfs_dfs(problem, frontier):
    parent = {}
    explored = set()
    frontier.push(problem.get_initial_state())
    parent[problem.get_initial_state()] = None
    
    while not frontier.is_empty():
        cur = frontier.pop()
        if cur in explored:
            continue
        explored.add(cur)
        if problem.is_goal_state(cur):
            p = cur
            path = []
            while parent[p]:
                move = parent[p][1]
                p = parent[p]
                path.append(move)
            path.reverse()
            return path
        for next_state in problem.get_neighbors(cur):
            state = next_state[0]
            if state not in explored and state not in frontier:
                parent[state] = (cur, next_state[1])
                frontier.push(state)
    return []
        
    