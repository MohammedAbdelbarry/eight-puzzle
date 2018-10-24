from typing import List, Any, Tuple


class SearchState:
    """
    Represents a search state
    """

    def next_state(self, action: Any) -> 'SearchState':
        """
        Returns the next state that results from applying the action to the current state
        :param action: Any object that represents an action
        :return: the next state that results from applying the action to the current state
        """
        raise NotImplementedError

    def get_neighbors(self) -> List[Tuple['SearchState', Any, float]]:
        """
        Returns a list of tuples (next_state, action, cost)
        :return: a list of tuples (next_state, action, cost)
        """
        raise NotImplementedError


class SearchProblem:
    """
    This class defines the structure of a search problem.
    """

    def get_initial_state(self) -> SearchState:
        """
        Returns the start state for the search problem.
        :return A SearchState instance representing the initial state
        """
        raise NotImplementedError

    def is_goal_state(self, state: SearchState) -> bool:
        """
        Returns True if  the state is a goal state.
        :param state: SearchState The state to be checked
        :return bool value indicating whether or not the state is a goal state
        """
        raise NotImplementedError

    def get_neighbors(self, state: SearchState) -> List[Tuple['SearchState', Any, float]]:
        """
        Returns a list of tuples (next_state, action, cost)
        :param state: A SearchState instance representing the current state
        :return: a list of tuples (next_state, action, cost)
        """
        raise NotImplementedError
