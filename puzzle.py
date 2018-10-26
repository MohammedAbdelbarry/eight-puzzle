from problem import SearchState, SearchProblem
import random
import util
from typing import List, Tuple


class PuzzleState(SearchState):
    """
    Class defining the state of an 8-puzzle game.
    """
    state: List[List[int]]
    empty_pos: Tuple[int, int]
    height: int
    width: int

    def __init__(self, state: List[List[int]]):
        self.state = state
        self.empty_pos = (-1, -1)
        self.height, self.width = len(state), len(state[0])
        for (i, row) in enumerate(self.state):
            for (j, elem) in enumerate(row):
                if elem == 0:
                    self.empty_pos = (i, j)

    def __str__(self):
        return '\n'.join([' '.join([str(elem) if elem != 0 else ' ' for elem in row]) for row in self.state])

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def next_state(self, move: str) -> 'PuzzleState':
        """
        Returns the next state that results from applying the action to the current state
        :param move: str object that represents an action
        :return: the next state that results from applying the action to the current state
        """
        i, j = self.empty_pos
        new_row, new_col = i, j
        new_state = [[elem for elem in row] for row in self.state]
        if move == 'N':
            new_row = i - 1
        elif move == 'S':
            new_row = i + 1
        elif move == 'W':
            new_col = j - 1
        elif move == 'E':
            new_col = j + 1
        else:
            raise ValueError('Invalid Move {}'.format(move))
        new_state[i][j] = self.state[new_row][new_col]
        new_state[new_row][new_col] = self.state[i][j]
        return PuzzleState(new_state)

    def get_neighbors(self) -> List[Tuple['PuzzleState', str, float]]:
        """
        Returns a list of tuples (next_state, action, cost)
        :return: a list of tuples (next_state, action, cost)
        """
        next_states = []
        i, j = self.empty_pos
        row = self.state[i]
        elem = row[j]
        if elem == 0:
            if i != self.height - 1:
                next_states.append((self.next_state('S'), 'S', 1))
            if i != 0:
                next_states.append((self.next_state('N'), 'N', 1))
            if j != self.width - 1:
                next_states.append((self.next_state('E'), 'E', 1))
            if i != 0:
                next_states.append((self.next_state('W'), 'W', 1))

        return next_states


class PuzzleProblem(SearchProblem):

    puzzle: PuzzleState

    def __init__(self, puzzle: PuzzleState=None, width: int=3, height: int=3):
        self.puzzle = puzzle
        if not puzzle:
            p = list(range(0, width * height))
            random.shuffle(p)
            step = width
            self.puzzle = PuzzleState([p[i: i + step] for i in range(0, width * height, width)])

    def __eq__(self, other):
        return self.puzzle == other.puzzle

    def get_initial_state(self) -> PuzzleState:
        """
        Returns the start state for the search problem.
        :return A PuzzleState instance representing the initial state
        """
        return self.puzzle

    def is_goal_state(self, state: PuzzleState) -> bool:
        """
        Returns True if  the state is a goal state.
        :param state: PuzzleState The state to be checked
        :return bool value indicating whether or not the state is a goal state
        """
        return util.is_sorted([elem for row in state.state for elem in row])

    def get_neighbors(self, state: PuzzleState) -> List[Tuple['PuzzleState', str, float]]:
        """
        Returns a list of tuples (next_state, action, cost)
        :param state: A PuzzleState instance representing the current state
        :return: a list of tuples (next_state, action, cost)
        """
        return state.get_neighbors()
