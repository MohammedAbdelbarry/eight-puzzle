from puzzle import PuzzleState


def manhattan_distance_heuristic(state: PuzzleState):
    manhattan_distance_sum = 0
    for i in range(state.height):
        for j in range(state.width):
            manhattan_distance_sum += abs(i - state.state[i][j] / state.height) \
                + abs(j - state.state[i][j] % state.width)
    return manhattan_distance_sum


def euclidean_distance_heuristic(state: PuzzleState):
    euclidean_distance_sum = 0
    for i in range(state.height):
        for j in range(state.width):
            euclidean_distance_sum += ((i - state.state[i][j] / state.height) ** 2 \
                + (j - state.state[i][j] % state.width) ** 2) ** 0.5
    return euclidean_distance_sum
