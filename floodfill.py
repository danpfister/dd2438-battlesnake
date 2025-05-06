from collections import deque
import utils


def flood_fill_max_area(game_state: dict, start: tuple) -> int:
    start = tuple(start)

    q = deque([start])
    visited = {start}
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  

    free_fields = utils.get_free_fields(game_state)

    max_distance = 0 

    while q:
        cur = q.popleft()

        for dx, dy in directions:
            nx, ny = cur[0] + dx, cur[1] + dy
            next_pos = (nx, ny)

            if next_pos not in free_fields or next_pos in visited:
                continue

            visited.add(next_pos)
            q.append(next_pos)
            max_distance += 1

    return max_distance

