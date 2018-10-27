from puzzle import PuzzleProblem, PuzzleState
from search import bfs, dfs, astar, ucs
from heuristic import manhattan_distance_heuristic, euclidean_distance_heuristic
from visualizer import Visualizer


if __name__ == '__main__':
    puzzle = PuzzleProblem(PuzzleState([[1, 0, 2], [3, 4, 5], [6, 7, 8]]))
    #puzzle = PuzzleProblem()
    print(puzzle.puzzle)
    path, explored_states_count = bfs(puzzle)
    print("Number of explored states: " + str(explored_states_count) + "\n")
    print("Cost of the solution: " + str(len(path) - 1))
    Visualizer(path).play()

