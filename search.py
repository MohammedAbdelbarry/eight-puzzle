from problem import SearchState, SearchProblem
from typing import List, Callable
from util import Stack, Queue, PriorityQueue


def bfs_dfs(problem, frontier):
    parent = {}
    explored = set()
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
            return path
        for next_state in problem.get_neighbors(cur):
            state = next_state[0]
            if state not in explored:
                parent[state] = cur
                frontier.push(state)
                explored.add(state)
                
    return []
        

def ucs_astar(problem, frontier, heuristic):
    parent = {}
    cost = {}
    explored = set()
    frontier.push(problem.get_initial_state(), 0 + heuristic(problem.get_initial_state(), problem))
    parent[problem.get_initial_state()] = None
    cost[problem.get_initial_state()] = 0
    
    while not frontier.is_empty():
        cur = frontier.pop()
        explored.add(cur)
        print("State to explore: \n\n" + str(cur) + '\n')
        if problem.is_goal_state(cur):
            p = cur
            path = []
            while parent[p]:
                move = parent[p][1]
                p = parent[p][0]
                path.append(move)
            path.reverse()
            return path
        for next_state in problem.get_neighbors(cur):
            state = next_state[0]
            if state not in explored and state not in frontier:
                parent[state] = (cur, next_state[1])
                cost[state] = cost[cur] + next_state[2]
                frontier.push(state, cost[state] + heuristic(state, problem))
            elif state in frontier:
                if cost[state] > cost[cur] + next_state[2]:
                    parent[state] = (cur, next_state[1])
                    cost[state] = cost[cur] + next_state[2]
                    frontier.update(state, cost[state] + heuristic(state, problem))
                    
    return []


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
    raise ucs_astar(problem, PriorityQueue(), None)


def astar(problem: SearchProblem, heuristic: Callable[[SearchState, SearchProblem], float]) -> List[SearchState]:
    """
    Returns the path from the initial state of the problem to a goal state.
    :param problem: a SearchProblem
    :return: List[SearchState] representing the path
    """
    return ucs_astar(problem, PriorityQueue(), None)