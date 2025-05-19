import typing
import floodfill
import numpy as np
from collections import deque

FOOD_WEIGHT = 0.7

def get_free_fields(game_state: dict, safe_mode=True):
    fields = set(
        (i, j)
        for i in range(game_state["board"]["width"])
        for j in range(game_state["board"]["height"])
    )
    moves = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}
    my_length = game_state["you"]["length"]
    our_head_cell = (game_state["you"]["body"][0]["x"], game_state["you"]["body"][0]["y"])
    
    for i, b in enumerate(game_state["you"]["body"]):
        cell = (b["x"], b["y"])
        # skip cells which won't be occupied by the time we reach them
        if get_distance(cell, our_head_cell) >= my_length - i: continue
        fields.discard((b["x"], b["y"]))
        
    for snake in game_state["board"]["snakes"]:
        if snake["id"] == game_state["you"]["id"]: continue
        head = snake["body"][0]
        snake_length = snake["length"]
        
        # in safe mode: for longer snakes discard cells where enemy head can move
        if snake_length >= my_length and safe_mode:
            for move in moves.values():
                fields.discard((head["x"] + move[0], head["y"] + move[1]))
                
        for i, b in enumerate(snake["body"]):
            cell = (b["x"], b["y"])
            if get_distance(cell, our_head_cell) >= snake_length - i: continue
            fields.discard((b["x"], b["y"]))
            
    return fields

def get_enemy_heads(game_state: dict):
    my_name = game_state["you"]["name"]
    return [
        {
            "pos": (snake["head"]["x"], snake["head"]["y"]),
            "length": snake["length"],
        }
        for snake in game_state["board"]["snakes"]
        if snake["name"] == my_name
    ]


def get_scores(game_state: dict, food_distances: dict, floodfill_distances: dict):
    # scale values to [0-1]
    food_distances = {k: max(0, 10 - v) for k, v in food_distances.items()}
    max_food_distance = max(max(food_distances.values()), 1)
    food_distances = {k: v / max_food_distance for k, v in food_distances.items()}
    
    floodfill_distances = {k: max(0, v - 7) for k, v in floodfill_distances.items()}
    max_floodfill_distance = max(max(floodfill_distances.values()), 1)
    floodfill_distances = {k: v / max_floodfill_distance for k, v in floodfill_distances.items()}
    
    my_head = (game_state["you"]["body"][0]["x"], game_state["you"]["body"][0]["y"])
    my_length = game_state["you"]["length"]
    enemy_heads = get_enemy_heads(game_state)
    move_to_delta = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}
    
    scores = {}
    for move in food_distances.keys():
        food_score = food_distances[move]
        space_score = floodfill_distances[move]

        if game_state["you"]["health"] < 25: # prevents snake from dying of hunger
            score = food_score
        score = FOOD_WEIGHT * food_score + (1 - FOOD_WEIGHT) * space_score

        # add offensive bonus
        dx, dy = move_to_delta[move]
        new_pos = (my_head[0] + dx, my_head[1] + dy)

        for enemy in enemy_heads:
            enemy_pos = enemy["pos"]
            dist = abs(new_pos[0] - enemy_pos[0]) + abs(new_pos[1] - enemy_pos[1])

            # head-to-head opportunities or risks
            if dist == 1:
                if my_length > enemy["length"]:
                    score += 0.3  

            # trap potential if you control more space
            enemy_area = floodfill.flood_fill_max_area(game_state, enemy_pos, move)

            if floodfill_distances[move] > (enemy_area / 10):  
                score += 0.2


        scores[move] = score
    
    return scores

def get_voronoi_numpy(width, height, snakes):
    # Constants
    UNCLAIMED = -1
    CONTESTED = -2

    # Initialize arrays
    owner_map = np.full((width, height), UNCLAIMED, dtype=np.int32)
    distance_map = np.full((width, height), np.inf, dtype=np.float32)
    blocked = np.zeros((width, height), dtype=bool)

    # Map snake IDs to indices
    snake_id_map = {snake['id']: idx for idx, snake in enumerate(snakes)}
    reverse_id_map = {v: k for k, v in snake_id_map.items()}

    queue = deque()

    # Mark blocked cells and queue snake heads
    for snake in snakes:
        idx = snake_id_map[snake['id']]
        for segment in snake['body']:
            x, y = segment['x'], segment['y']
            blocked[x, y] = True
        head_x, head_y = snake['head']['x'], snake['head']['y']
        if not blocked[head_x, head_y]:
            queue.append((head_x, head_y, idx, 0))
            owner_map[head_x, head_y] = idx
            distance_map[head_x, head_y] = 0

    # BFS directions
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        x, y, idx, dist = queue.popleft()

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            if blocked[nx, ny]:
                continue

            if distance_map[nx, ny] > dist + 1:
                distance_map[nx, ny] = dist + 1
                owner_map[nx, ny] = idx
                queue.append((nx, ny, idx, dist + 1))
            elif distance_map[nx, ny] == dist + 1 and owner_map[nx, ny] != idx:
                owner_map[nx, ny] = CONTESTED

def get_distance(a, b):
    '''
    get manhattan distance between two cells of the type: (x, y)
    '''
    distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
    return distance