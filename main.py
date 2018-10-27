from puzzle import PuzzleProblem, PuzzleState
from search import bfs, dfs, astar, ucs
from heuristic import manhattan_distance_heuristic, euclidean_distance_heuristic
from visualizer import Visualizer


if __name__ == '__main__':
    puzzle = PuzzleProblem(width=3, height=3)
    path, explored_states_count = dfs(puzzle)
    if not path:
        print('No solution was found for the puzzle:\n%s' % str(puzzle.puzzle))
        exit(1)
    print()
    print("Number of explored states: %d" % explored_states_count)
    print()
    print("Cost of the solution: " + str(len(path) - 1))
    Visualizer(path).play()

