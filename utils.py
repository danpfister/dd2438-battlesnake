import typing

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

def get_scores(game_state: dict, food_distances: dict, floodfill_distances: dict):
    # scale values to [0-1]
    food_distances = {k: max(0, 10 - v) for k, v in food_distances.items()}
    max_food_distance = max(max(food_distances.values()), 1)
    food_distances = {k: v / max_food_distance for k, v in food_distances.items()}
    
    floodfill_distances = {k: (v - 5) for k, v in floodfill_distances.items()}
    max_floodfill_distance = max(max(floodfill_distances.values()), 1)
    floodfill_distances = {k: v / max_floodfill_distance for k, v in floodfill_distances.items()}
    
    scores = {}
    for move in food_distances.keys():
        if game_state["you"]["health"] < 25: # prevents snake from dying of hunger
            scores[move] = food_distances[move]
        else:
            scores[move] = FOOD_WEIGHT * food_distances[move] + (1 - FOOD_WEIGHT) * floodfill_distances[move]
    
    return scores

def get_distance(a, b):
    '''
    get manhattan distance between two cells of the type: (x, y)
    '''
    distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
    return distance