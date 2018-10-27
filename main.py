from puzzle import PuzzleProblem, PuzzleState
from search import bfs, dfs, astar, ucs
from heuristic import manhattan_distance_heuristic, euclidean_distance_heuristic
from visualizer import Visualizer
import time


if __name__ == '__main__':
    puzzle = PuzzleProblem(PuzzleState([[3, 1, 2], [4, 0, 5], [6, 7, 8]]))
    #puzzle = PuzzleProblem()
    print("Initial Puzzle State")
    print()
    print(puzzle.puzzle)
    start_time = time.time()
    path, explored_states_count, maximum_depth_reached = bfs(puzzle)
    end_time = time.time()
    if not path:
        print('No solution was found for the puzzle:\n%s' % str(puzzle.puzzle))
        exit(1)
    print()
    print("Number of explored states: %d" % explored_states_count)
    print()
    print("Cost of the solution: %d" % (len(path) - 1))
    print()
    print("Maximum depth reached: %d" % maximum_depth_reached)
    print()
    print("Running time(seconds): %f" % (end_time - start_time))
    Visualizer(path).play()

