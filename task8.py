
from queue import PriorityQueue
from time import perf_counter

goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def misplaced(state):
    count = 0

    for i in range(9):
        if state[i] != 0 and state[i] != goal[i]:
            count += 1

    return count


def manhattan(state):
    distance = 0

    for i in range(9):
        tile = state[i]

        if tile != 0:
            target = tile - 1
            distance += abs(i // 3 - target // 3)
            distance += abs(i % 3 - target % 3)

    return distance


def solvable(state):
    tiles = [x for x in state if x != 0]
    inversions = 0

    for i in range(8):
        for j in range(i + 1, 8):
            if tiles[i] > tiles[j]:
                inversions += 1

    return inversions % 2 == 0


def neighbours(state):
    empty = state.index(0)
    row, col = empty // 3, empty % 3
    result = []

    for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        r, c = row + dr, col + dc

        if 0 <= r < 3 and 0 <= c < 3:
            new = list(state)
            other = r * 3 + c

            new[empty], new[other] = new[other], new[empty]
            result.append(tuple(new))

    return result


def a_star(start, heuristic):
    if not solvable(start):
        return None, 0

    queue = PriorityQueue()
    queue.put((heuristic(start), 0, start))

    best_cost = {start: 0}
    expanded = 0

    while not queue.empty():
        score, cost, state = queue.get()

        if cost != best_cost[state]:
            continue

        expanded += 1

        if state == goal:
            return cost, expanded

        for neighbour in neighbours(state):
            new_cost = cost + 1

            if new_cost < best_cost.get(neighbour, float('inf')):
                best_cost[neighbour] = new_cost
                score = new_cost + heuristic(neighbour)
                queue.put((score, new_cost, neighbour))

    return None, expanded


states = [
    (1, 2, 3, 4, 5, 6, 7, 0, 8),
    (1, 2, 3, 4, 5, 6, 0, 7, 8),
    (1, 3, 6, 4, 2, 8, 7, 5, 0),
    (1, 2, 3, 4, 5, 6, 8, 7, 0),
    (2, 1, 3, 4, 5, 6, 7, 0, 8)
]


for number, state in enumerate(states, 1):
    print("\nTest", number)

    for i in range(0, 9, 3):
        print(state[i:i + 3])

    print("Solvable:", solvable(state))

    for name, heuristic in [("Misplaced", misplaced),
                            ("Manhattan", manhattan)]:

        start_time = perf_counter()
        moves, expanded = a_star(state, heuristic)
        time_taken = (perf_counter() - start_time) * 1000

        print(name, "| Moves:", moves,
              "| Nodes:", expanded,
              "| Time: %.3f ms" % time_taken)


# Task 8 - Comparing the two heuristics

# Misplaced Tiles:
# Counts how many tiles are in the wrong position.
# We don't count the empty space.

# Manhattan Distance:
# Calculates how far each tile is from its correct place.
# It counts the horizontal and vertical moves needed.

# A* Search:
# Uses a priority queue to choose the next state.
# f = g + h
# g is the moves made so far.
# h is the estimated moves left.

# Testing:
# I tested 5 different puzzles.
# The first 3 can be solved, but the last 2 cannot.
# I compared the moves, nodes visited and time taken.

# Time and Space Complexity:
# A* can take exponential time and space in general.
# The 8-puzzle has a limited number of possible states.
# The priority queue stores states waiting to be checked.

# Conclusion:
# Both heuristics can find the shortest solution.
# Manhattan Distance usually works better because
# it considers how far each tile is from its goal.
# The program also checks if a puzzle is solvable
# before starting the search.
