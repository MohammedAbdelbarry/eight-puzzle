from problem import SearchState, SearchProblem
from typing import List, Callable


def bfs(problem: SearchProblem) -> List[SearchState]:
    """
    Returns the path from the initial state of the problem to a goal state.
    :param problem: a SearchProblem
    :return: List[SearchState] representing the path
    """
    raise NotImplementedError


def dfs(problem: SearchProblem) -> List[SearchState]:
    """
    Returns the path from the initial state of the problem to a goal state.
    :param problem: a SearchProblem
    :return: List[SearchState] representing the path
    """
    raise NotImplementedError


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

