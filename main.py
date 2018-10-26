from puzzle import PuzzleProblem, PuzzleState
from search import bfs, dfs, astar, ucs
from heuristic import manhattan_distance_heuristic, euclidean_distance_heuristic
from visualizer import Visualizer


if __name__ == '__main__':
    #puzzle = PuzzleProblem(PuzzleState([[5, 0, 8], [3, 6, 4], [2, 7, 1]]))
    puzzle = PuzzleProblem()
    print(puzzle.puzzle)
    path = astar(puzzle, euclidean_distance_heuristic)
    Visualizer(path).play()

