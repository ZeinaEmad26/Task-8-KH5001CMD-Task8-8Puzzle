
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


def linear_conflict(state):
    # Only count conflict pairs that do not share tiles.
    used = set()
    conflicts = 0

    for i in range(9):
        a = state[i]

        if a == 0 or a in used:
            continue

        for j in range(i + 1, 9):
            b = state[j]

            if b == 0 or b in used:
                continue

            row_conflict = (
                i // 3 == j // 3 == (a - 1) // 3 == (b - 1) // 3
                and (a - 1) % 3 > (b - 1) % 3
            )

            col_conflict = (
                i % 3 == j % 3 == (a - 1) % 3 == (b - 1) % 3
                and (a - 1) // 3 > (b - 1) // 3
            )

            if row_conflict or col_conflict:
                used.update((a, b))
                conflicts += 1
                break

    return manhattan(state) + 2 * conflicts


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
    if len(start) != 9 or set(start) != set(range(9)):
        raise ValueError(
            'The puzzle must contain each number from 0 to 8 once.'
        )

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


def get_case(number):
    if number == 1:
        return (1, 2, 3, 4, 5, 6, 7, 0, 8)
    elif number == 2:
        return (1, 2, 3, 4, 5, 6, 0, 7, 8)
    elif number == 3:
        return (1, 3, 6, 4, 2, 8, 7, 5, 0)
    elif number == 4:
        return (1, 2, 3, 4, 5, 6, 8, 7, 0)
    elif number == 5:
        return (2, 1, 3, 4, 5, 6, 7, 0, 8)
    else:
        raise ValueError('The case number must be from 1 to 5.')


def main():
    print('Case | Heuristic | Result | Moves | Nodes | Time (seconds)')

    for number in range(1, 6):
        state = get_case(number)

        print('\nTest', number)

        for i in range(0, 9, 3):
            print(state[i:i + 3])

        for name, heuristic in [
            ('Misplaced', misplaced),
            ('Manhattan', manhattan),
            ('Linear Conflict', linear_conflict)
        ]:
            start_time = perf_counter()
            moves, expanded = a_star(state, heuristic)
            time_taken = perf_counter() - start_time

            if moves is None:
                result = 'Unsolvable'
                moves_text = 'No solution'
            else:
                result = 'Solved'
                moves_text = str(moves)

            print(
                f'{number} | {name} | {result} | {moves_text} | '
                f'{expanded} | {time_taken:.9f}'
            )


if __name__ == '__main__':
    main()
