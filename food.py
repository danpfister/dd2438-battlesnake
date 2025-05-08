from collections import deque
import utils

def get_food_locations(game_state: dict):
    foods = set((f["x"], f["y"]) for f in game_state["board"]["food"])
    return foods

def get_food_distance(game_state: dict, start):
    queue = deque([(start, 0)]) # using double ended queue
    visited = set()
    
    foods = get_food_locations(game_state)
    free_fields = utils.get_free_fields(game_state)
    
    if len(foods) == 0: return 0
    
    while queue:
        current, dist = queue.popleft()
        if current in foods:
            return dist
        if current in visited:
            continue
        visited.add(current)
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = current[0] + dx, current[1] + dy
            if (nx, ny) in free_fields:
                queue.append(((nx, ny), dist + 1))
    
    return 1000; # no food found
        