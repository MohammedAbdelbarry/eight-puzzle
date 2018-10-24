from typing import List
from problem import SearchState


class Visualizer:

    def __init__(self, history: List[SearchState]):
        raise NotImplementedError

    def play(self) -> None:
        """
        Plays the visualization history of the game.
        """
        raise NotImplementedError