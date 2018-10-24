from puzzle import PuzzleProblem
from search import bfs
from visualizer import Visualizer


if __name__ == '__main__':
    puzzle = PuzzleProblem()
    path = bfs(puzzle)
    Visualizer(path).play()

